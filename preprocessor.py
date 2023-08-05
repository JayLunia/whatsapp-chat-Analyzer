import re
import pandas as pd

# def preprocess(data):
#     pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

#     messages = re.split(pattern, data)[1:]
#     dates = re.findall(pattern, data)

#     df = pd.DataFrame({'user_message': messages, 'message_date': dates})
#     # convert message_date type
#     df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')

#     df.rename(columns={'message_date': 'date'}, inplace=True)

#     users = []
#     messages = []
#     for message in df['user_message']:
#         entry = re.split('([\w\W]+?):\s', message)
#         if entry[1:]:  # user name
#             users.append(entry[1])
#             messages.append(" ".join(entry[2:]))
#         else:
#             users.append('group_notification')
#             messages.append(entry[0])

#     df['user'] = users
#     df['message'] = messages
#     df.drop(columns=['user_message'], inplace=True)

#     df['only_date'] = df['date'].dt.date
#     df['year'] = df['date'].dt.year
#     df['month_num'] = df['date'].dt.month
#     df['month'] = df['date'].dt.month_name()
#     df['day'] = df['date'].dt.day
#     df['day_name'] = df['date'].dt.day_name()
#     df['hour'] = df['date'].dt.hour
#     df['minute'] = df['date'].dt.minute

#     period = []
#     for hour in df[['day_name', 'hour']]['hour']:
#         if hour == 23:
#             period.append(str(hour) + "-" + str('00'))
#         elif hour == 0:
#             period.append(str('00') + "-" + str(hour + 1))
#         else:
#             period.append(str(hour) + "-" + str(hour + 1))

#     df['period'] = period

#     return df


def preprocess(data):
    pattern = r"(\d{1,2}\/\d{1,2}\/\d{2}), (\d{1,2}:\d{2}\s*[AP]M) - ([\s\w@$!%*#?&\']+):\s(.+)"

    table = []
    for line in data.splitlines():
        match = re.match(pattern, line)
        if match:
            date = match.group(1)
            time = match.group(2)
            sender = match.group(3)
            message = match.group(4)
            table.append({'Date': date, 'Time': time, 'user': sender, 'message': message})

    df=pd.DataFrame(table)
    df.Date=pd.to_datetime(df.Date)
    df.Time=pd.to_datetime(df.Time,format="%I:%M %p").dt.strftime("%H:%M")
    df['hour']=df.Time.apply(lambda x: int(x.split(':')[0]))
    df['minute']=df.Time.apply(lambda x: int(x.split(':')[1]))
    df['year']=df['Date'].dt.year
    df['month_num']=df['Date'].dt.month
    df['month']=df['Date'].dt.month_name()
    df['day']=df['Date'].dt.day
    df['day_name']=df['Date'].dt.day_name()
    df['only_date']=df['Date'].dt.date
    df.drop(['Date','Time'],axis=1,inplace=True)
    
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df