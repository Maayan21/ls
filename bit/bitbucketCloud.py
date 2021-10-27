import json
import socket
from requests import Session
from bs4 import BeautifulSoup as BS
import os

username = '4200cmp'  # your admin username
password = '42002020'  # your app password https://support.atlassian.com/bitbucket-cloud/docs/app-passwords/
workspace = '4200cmp'  # your workspace ID https://support.atlassian.com/bitbucket-cloud/docs/change-a-workspace-id/
cookie1='ajs_anonymous_id="d47e55cc-9bdd-4771-8d65-53a58414b7e7"; _ga=GA1.2.521642193.1630319415; atl_xid.current=[{"type":"xc","value":"ef0643f9-6b91-4c16-b7a1-109145a8f112","createdAt":"2021-08-17T22:33:31.037Z"}]; atlCohort={"bucketAll":{"bucketedAtUTC":"2021-08-30T10:30:15.552Z","version":"2","index":1,"bucketId":0}}; _sio=d47e55cc-9bdd-4771-8d65-53a58414b7e7; atlUserHash=1393648548; _gcl_au=1.1.373704135.1630319416; _mkto_trk=id:594-ATC-127&token:_mch-bitbucket.org-1630319416863-29333; _fbp=fb.1.1630319417188.881921305; ajs_group_id=null; optimizelyEndUserId=oeu1633597507604r0.6608013335166001; atl_xid.ts=1633597508868; _pxvid=aa978632-274d-11ec-a206-486370775441; __stripe_mid=e61504b4-6fd7-4f3f-a65f-d2c43a97efd54761be; OptanonConsent=landingPath=NotLandingPage&datestamp=Thu+Oct+07+2021+14:26:04+GMT+0300+(Israel+Daylight+Time)&version=4.6.0&EU=false&groups=1:1,2:1,3:1,4:1,0_147330:1,0_155512:1,0_173487:1,0_173483:1,0_145889:1,0_173485:1,0_146517:1,0_144595:1,0_155516:1,0_155514:1,0_172277:1,0_155513:1,0_173486:1,0_162898:1,0_145888:1,0_173482:1,0_173484:1,0_144594:1,0_150453:1,0_173480:1,0_155515:1,101:1,117:1,120:1,144:1,160:1,180:1&AwaitingReconsent=false; csrftoken=3GCRHBeCkuA69407BPjpjRf31KmlvJypEnzSTEoUIWj0gPuRz3txU1g1L6rjZUEa; pxcts=f51146d0-2952-11ec-b8f7-df035ea4668a; _gid=GA1.2.1934031190.1634043013; _uetvid=446bca10097d11ecba494d7c46d1ab32; _px3=7d42b53cf1dbda8252cd5da25f1ed85b24945fa644a1251840b8753b9e66d2d6:htjaQ87NjzhBymDC3AMy0OWRe4aVDmaYMMKhYp+Q3/MAJIiNWlUGpWJgzWeS6UmFYc6gJAGNZqJwOkNgG5Bjxw==:1000:o7tIZxaMDM5TDRF8j++k1MoY7oKQlaAAGLVt92X0bH1lWo0vXQlYrMiFmq3dfbW2PKVDu2T1LVUIv0P4zwZOB1cUWaXUL22hxquK0B+ikxeHicxsnL7qH7BXzmtQMWnp7whvrdDpryaOhI0P6Gj+sOLQz2hjyF7IFVMimPEfFamVuftOhORjtJumT8PSqmvSa6WCxOIqvXdKEZbXpT2ioA==; cloud.session.token=eyJraWQiOiJzZXNzaW9uLXNlcnZpY2VcL3Byb2QtMTU5Mjg1ODM5NCIsImFsZyI6IlJTMjU2In0.eyJhc3NvY2lhdGlvbnMiOlt7ImFhSWQiOiI2MTEyNTg5YjYyN2I1NjAwNjg2ZjNjNjIiLCJzZXNzaW9uSWQiOiJlNDEyMTFlMy0xODVlLTRlZDEtOTg1OS04NTQwYzU2NmQ5Y2EiLCJlbWFpbCI6Im1hYXlhbi5jb2hlbkBjeWJlcnNhZmUuY28uaWwifSx7ImFhSWQiOiI1ZWY4N2QxZDM0MDQ2OTBiYWU3MWU5YTUiLCJzZXNzaW9uSWQiOiJhYWE1ZDQ0OS0wM2M1LTRjNmQtYjFhNi02ZDI4YTBmZTEwZmQiLCJlbWFpbCI6Im1hYXlhbjIwNjlAZ21haWwuY29tIn1dLCJzdWIiOiI2MTVlZDkwMjJmNmFlZDAwNjhjMTBlM2QiLCJlbWFpbERvbWFpbiI6ImdtYWlsLmNvbSIsImltcGVyc29uYXRpb24iOltdLCJjcmVhdGVkIjoxNjMzNjA1OTU5LCJyZWZyZXNoVGltZW91dCI6MTYzNDEzOTk2OCwidmVyaWZpZWQiOnRydWUsImlzcyI6InNlc3Npb24tc2VydmljZSIsInNlc3Npb25JZCI6IjhkNmQ3ZDUxLTkzZjItNDBkZC1hODk2LTkzOWQzZTE1M2Y4YiIsImF1ZCI6ImF0bGFzc2lhbiIsIm5iZiI6MTYzNDEzOTM2OCwiZXhwIjoxNjM2NzMxMzY4LCJpYXQiOjE2MzQxMzkzNjgsImVtYWlsIjoiNDIwMGNtcEBnbWFpbC5jb20iLCJqdGkiOiI4ZDZkN2Q1MS05M2YyLTQwZGQtYTg5Ni05MzlkM2UxNTNmOGIifQ.zu8NImhiyj-Mp1B28zp1TwilmUP_8JRBveZIuNwP6_1awumZpALBateyZcqseproJQWlUS8H6zon7If6aGOU93yeTzjQ52RuKRcBVGyidkA38RYNtKyf6fPiLHFCdKh5utZzeAoNi100PTTMkvMcFVBS81wijCcKFtURGZRQod0detavxV3BW2-DP9wNavs5x3UjmJlUTN8r0dpQASYvJUt1WLS9xqQNXRqI0A3Xu8JDQIuQCcs3ZOuaIrH0W66l2d1XoqveCfjw0Md9MJI96q53ETnP5g1ct32SQvHDxQ-bmfNk6INiNvT3679opcADkAAVuo9JgrKbMHnHPPrrxg'
cookie='ajs_anonymous_id="d47e55cc-9bdd-4771-8d65-53a58414b7e7"; _ga=GA1.2.521642193.1630319415; atl_xid.current=[{"type":"xc","value":"ef0643f9-6b91-4c16-b7a1-109145a8f112","createdAt":"2021-08-17T22:33:31.037Z"}]; atlCohort={"bucketAll":{"bucketedAtUTC":"2021-08-30T10:30:15.552Z","version":"2","index":1,"bucketId":0}}; _sio=d47e55cc-9bdd-4771-8d65-53a58414b7e7; atlUserHash=1393648548; _gcl_au=1.1.373704135.1630319416; _mkto_trk=id:594-ATC-127&token:_mch-bitbucket.org-1630319416863-29333; _fbp=fb.1.1630319417188.881921305; ajs_group_id=null; optimizelyEndUserId=oeu1633597507604r0.6608013335166001; atl_xid.ts=1633597508868; _pxvid=aa978632-274d-11ec-a206-486370775441; __stripe_mid=e61504b4-6fd7-4f3f-a65f-d2c43a97efd54761be; csrftoken=3GCRHBeCkuA69407BPjpjRf31KmlvJypEnzSTEoUIWj0gPuRz3txU1g1L6rjZUEa; _px3=7d42b53cf1dbda8252cd5da25f1ed85b24945fa644a1251840b8753b9e66d2d6:htjaQ87NjzhBymDC3AMy0OWRe4aVDmaYMMKhYp+Q3/MAJIiNWlUGpWJgzWeS6UmFYc6gJAGNZqJwOkNgG5Bjxw==:1000:o7tIZxaMDM5TDRF8j++k1MoY7oKQlaAAGLVt92X0bH1lWo0vXQlYrMiFmq3dfbW2PKVDu2T1LVUIv0P4zwZOB1cUWaXUL22hxquK0B+ikxeHicxsnL7qH7BXzmtQMWnp7whvrdDpryaOhI0P6Gj+sOLQz2hjyF7IFVMimPEfFamVuftOhORjtJumT8PSqmvSa6WCxOIqvXdKEZbXpT2ioA==; OptanonConsent=landingPath=NotLandingPage&datestamp=Thu+Oct+14+2021+12:03:36+GMT+0300+(Israel+Daylight+Time)&version=4.6.0&EU=false&groups=1:1,2:1,3:1,4:1,0_147330:1,0_155512:1,0_173487:1,0_173483:1,0_145889:1,0_173485:1,0_146517:1,0_144595:1,0_155516:1,0_155514:1,0_172277:1,0_155513:1,0_173486:1,0_162898:1,0_145888:1,0_173482:1,0_173484:1,0_144594:1,0_150453:1,0_173480:1,0_155515:1,101:1,117:1,120:1,144:1,160:1,180:1&AwaitingReconsent=false; _uetvid=446bca10097d11ecba494d7c46d1ab32; cloud.session.token=eyJraWQiOiJzZXNzaW9uLXNlcnZpY2VcL3Byb2QtMTU5Mjg1ODM5NCIsImFsZyI6IlJTMjU2In0.eyJhc3NvY2lhdGlvbnMiOlt7ImFhSWQiOiI1ZWY4N2QxZDM0MDQ2OTBiYWU3MWU5YTUiLCJzZXNzaW9uSWQiOiJiMDM0ZWEwZC1jN2M5LTRmNjQtYTEwZC1mZjUxZDBmNTQ3OWIiLCJlbWFpbCI6Im1hYXlhbjIwNjlAZ21haWwuY29tIn0seyJhYUlkIjoiNjExMjU4OWI2MjdiNTYwMDY4NmYzYzYyIiwic2Vzc2lvbklkIjoiZmZlYzE5NjItZDBhNy00YTIyLWFiNTktNDE2M2FkYWZmMjE3IiwiZW1haWwiOiJtYWF5YW4uY29oZW5AY3liZXJzYWZlLmNvLmlsIn1dLCJzdWIiOiI2MTVlZDkwMjJmNmFlZDAwNjhjMTBlM2QiLCJlbWFpbERvbWFpbiI6ImdtYWlsLmNvbSIsImltcGVyc29uYXRpb24iOltdLCJjcmVhdGVkIjoxNjM0MjExMTMzLCJyZWZyZXNoVGltZW91dCI6MTYzNTE4NjE3OCwidmVyaWZpZWQiOnRydWUsImlzcyI6InNlc3Npb24tc2VydmljZSIsInNlc3Npb25JZCI6ImI5ZTVjNzYyLWM4ZTAtNGIzYy1hNThjLWMxNzZlMDEzZDc3NSIsImF1ZCI6ImF0bGFzc2lhbiIsIm5iZiI6MTYzNTE4NTU3OCwiZXhwIjoxNjM3Nzc3NTc4LCJpYXQiOjE2MzUxODU1NzgsImVtYWlsIjoiNDIwMGNtcEBnbWFpbC5jb20iLCJqdGkiOiJiOWU1Yzc2Mi1jOGUwLTRiM2MtYTU4Yy1jMTc2ZTAxM2Q3NzUifQ.ow25J4U9M7m2uZHhB5OKNBh_6C0tXmkATym6vxfXOjjn8aVpIttoGBD70U65kt-M5t72oEjHyeryjuRRFXHlOqKpikHDeUIfNb9mq3oJzJeN64QEaQ5xoYha7qVq4Xu3kMUay2YX1Ruf7-AdWteA09MLynkn7BPFNKDIlvnF6aNhxwxG-9xbM4BxZ6gIwRYL8DqyTAeLT5Mm77S4NpZ_m4c-9qtrJtdG_KD_SJjhC3SwhbpA73WkcYRBogNMUXhxvwYuytbwcbwAYaTe8uJ0Y88IirxQ0XNlWHUj_GZaqNP2PJ8t7mzNtRN9HAxVJcPnUfMnneipF7bD8HTzvpx2OA; __stripe_sid=cf5e4482-53fb-478a-82f7-beb125f6a3dfc18d22; _gid=GA1.2.869562330.1635185604'
HOST = os.getenv("HOST")  # Standard loopback interface address (localhost)
PORT = 4045
def build_session():
    session = Session()
    session.auth = (username, password)
    return session, workspace


def get_audit_log_activity(session, workspace, page=None, limit=None):
    while True:
        headers = {'cookie': cookie}
        params = {'page': page, 'iframe': 'true', 'spa': 0}
        url = f"https://bitbucket.org/{workspace}/workspace/settings/auditlog"
        r = session.get(url, params=params, headers=headers)
        soup = BS(r.text, 'html.parser')
        activity_list = soup.find('div', class_='activity-list')
        items=activity_list.find_all('article', class_='activity-item')
        for item in items:
            timestamp = item.find('time').text.strip()
            timestamp1 = str(item.find('time'))
            p=timestamp1.find('datetime')
            p2=timestamp1.find('>')
            totaltime=timestamp1[p+10:p2-1]          
            ip = item.find('span', class_='user-ip').text.strip()  
            full_action = ''
            for div in item.find_all('div'):
                if full_action == '':
                    full_action += ' '.join(div.text.split())
                else:
                    full_action += f'  ({" ".join(div.text.split())})'
            yield totaltime, full_action,ip
        
        if page is None:
            page = 1
        
        next_button = soup.find('li', class_="aui-nav-next")
        if 'aria-disabled="true"' in str(next_button):
            return
        else:
            page += 1

def main():
    session, workspace = build_session()
    record_counter = 0
    with open('c/Users/This_User/Desktop/audit_log.txt','r',encoding="utf-8") as _ids_list:
        _ids_list=_ids_list.readlines()
        # print(_ids_list)
    # print(json.dumps(_ids_list).encode('utf-8'))
    with open('c/Users/This_User/Desktop/audit_log.txt', '+a',encoding="utf-8") as out_file:
        for totaltime, full_action,ip in get_audit_log_activity(session, workspace):
            st={"timestamp": totaltime, "summary": full_action, "IP": ip}
            print(_ids_list)
            if str(st)+"\n" in _ids_list:
                print("old logs\n")
            else:
                print("new events"+str(st)+"\n")
                # print(str(st)+"\n")
                # out_file.write(str(st)+"\n")
                # record_counter += 1
                # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # sock.connect((HOST, PORT))
                # sock.send(json.dumps(st).encode("utf-8"))
                # sock.close()
            # print(f'Written {record_counter} records...')
    # exit(f"Complete. Written {record_counter} total records to ./audit_log.txt. Closing...")


if __name__ == '__main__':
    main()


