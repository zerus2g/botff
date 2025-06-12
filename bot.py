import os
import requests
from flask import Flask, request
import json

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', 'YOUR_BOT_TOKEN')
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}'

INFO_API_URL = 'https://api-info-nxx.onrender.com/info?id={user_id}'

# Dữ liệu tài khoản mẫu
SAMPLE_ACCOUNT_INFO = {
    "basicInfo": {
        "accountId": "6649999004",
        "accountType": 1,
        "nickname": "PNLㅤTxxG",
        "region": "ME",
        "level": 61,
        "exp": 1090471,
        "headPic": 902039007,
        "rank": 308,
        "rankingPoints": 1777,
        "badgeCnt": 1,
        "badgeId": 1001000085,
        "seasonId": 45,
        "liked": 7683,
        "showRank": True,
        "lastLoginAt": "1749587635",
        "csRank": 306,
        "csRankingPoints": 18,
        "weaponSkinShows": [907102426],
        "pinId": 910037001,
        "maxRank": 308,
        "csMaxRank": 306,
        "accountPrefers": {},
        "createAt": "1657971368",
        "title": 904590052,
        "externalIconInfo": {
            "status": "ExternalIconStatus_NOT_IN_USE",
            "showType": "ExternalIconShowType_FRIEND"
        },
        "releaseVersion": "OB49",
        "showBrRank": True,
        "showCsRank": True,
        "socialHighLightsWithBasicInfo": {}
    },
    "profileInfo": {
        "avatarId": 102000019,
        "clothes": [50],
        "equipedSkills": [214041009, 204000090, 211000164, 205041039, 203041046, 211000093],
        "pvePrimaryWeapon": 1,
        "endTime": 1,
        "isMarkedStar": True
    },
    "clanBasicInfo": {
        "clanId": "3052070118",
        "clanName": "PeaceNLives",
        "captainId": "5522938439",
        "clanLevel": 3,
        "capacity": 50,
        "memberNum": 26
    },
    "captainBasicInfo": {
        "accountId": "5522938439",
        "accountType": 1,
        "nickname": "PNLㅤB00B'SG",
        "region": "ME",
        "level": 62,
        "exp": 1290332,
        "bannerId": 901042014,
        "headPic": 902034024,
        "rank": 324,
        "rankingPoints": 4975,
        "badgeCnt": 46,
        "badgeId": 1001000085,
        "seasonId": 45,
        "liked": 6172,
        "lastLoginAt": "1749599097",
        "csRank": 307,
        "csRankingPoints": 23,
        "weaponSkinShows": [912036003],
        "pinId": 910039001,
        "maxRank": 324,
        "csMaxRank": 307,
        "accountPrefers": {},
        "createAt": "1646332324",
        "title": 904090022,
        "externalIconInfo": {
            "status": "ExternalIconStatus_NOT_IN_USE",
            "showType": "ExternalIconShowType_FRIEND"
        },
        "releaseVersion": "OB49",
        "showBrRank": True,
        "showCsRank": True,
        "socialHighLightsWithBasicInfo": {}
    },
    "petInfo": {
        "id": 1300000114,
        "name": "extra",
        "level": 7,
        "exp": 6009,
        "isSelected": True,
        "skinId": 1310000142,
        "selectedSkillId": 1315000013
    },
    "socialInfo": {
        "accountId": "6649999004",
        "language": "Language_FRENCH",
        "signature": "TIKTOK : @THUG4FF \nDON'T CRY",
        "rankShow": "RankShow_CS"
    },
    "diamondCostRes": {
        "diamondCost": 390
    },
    "creditScoreInfo": {
        "creditScore": 100,
        "rewardState": "REWARD_STATE_UNCLAIMED",
        "periodicSummaryEndTime": "1749650629"
    }
}

# Hàm định dạng thông tin tài khoản cho dễ đọc

def format_account_info(info):
    basic = info.get('basicInfo', {})
    clan = info.get('clanBasicInfo', {})
    pet = info.get('petInfo', {})
    signature = info.get('socialInfo', {}).get('signature', '')
    diamond = info.get('diamondCostRes', {}).get('diamondCost', '-')
    return (
        "🎮 THÔNG TIN TÀI KHOẢN\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"👤 Nickname: {basic.get('nickname')}\n"
        f"🏅 Level: {basic.get('level')}\n"
        f"⭐ Rank: {basic.get('rank')}\n"
        f"❤️ Lượt thích: {basic.get('liked')}\n"
        "\n"
        f"🏆 Clan: {clan.get('clanName', 'Không có')}\n"
        f"🐾 Pet: {pet.get('name', 'Không có')} (Lv.{pet.get('level', '-')})\n"
        "\n"
        f"💎 Kim cương đã tiêu: {diamond}\n"
        f"📝 Chữ ký: {signature}\n"
        "━━━━━━━━━━━━━━━━━━"
    )

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')
        
        if text.startswith('/info'):
            # Tách uid từ lệnh /info
            parts = text.split()
            if len(parts) > 1:
                uid = parts[1]
                # Lấy thông tin từ API với uid được cung cấp
                info = get_user_info(uid)
                if info:
                    try:
                        # Parse JSON response và format thông tin
                        account_info = json.loads(info)
                        formatted_info = format_account_info(account_info)
                        send_message(chat_id, formatted_info)
                    except json.JSONDecodeError:
                        send_message(chat_id, "Không thể lấy thông tin tài khoản. Vui lòng thử lại sau.")
                else:
                    send_message(chat_id, "Không tìm thấy thông tin tài khoản.")
            else:
                send_message(chat_id, "Vui lòng nhập uid sau lệnh /info. Ví dụ: /info 123456789")
        else:
            send_message(chat_id, "Sử dụng lệnh /info + uid để xem thông tin tài khoản")
    return {'ok': True}

def get_user_info(user_id):
    try:
        resp = requests.get(INFO_API_URL.format(user_id=user_id), timeout=5)
        if resp.status_code == 200:
            return resp.text
        else:
            return f'Lỗi API: {resp.status_code}'
    except Exception as e:
        return f'Lỗi khi gọi API: {e}'

def send_message(chat_id, text):
    url = f'{TELEGRAM_API_URL}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f'Lỗi gửi tin nhắn: {e}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 