from slitherlib.user_agent.ua import UserAgent

user_agent = UserAgent(thread_count='all').thread_uas

for i in user_agent:
    print(i)