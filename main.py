from core import Logger
from core import AccountManager
from core import Banner


def setup(log: Logger) -> AccountManager:
    log.info('Authenticating 🪪')
    
    try:
        am = AccountManager()
        log.success('Authenticated ✅')
    except:
        log.error('Error authenticating ⛔')
        
    return am


def main() -> None:
    print(Banner())
    log = Logger()
    
    root_am = setup(log)
    log.info(f"User ID: {root_am.user_id}")
    log.info(f"Username: {root_am.username}")
    log.info(f"Country: {root_am.country}")
    log.info(f"Email: {root_am.email}")
    log.info(f"User Type: {root_am.user_type}")
    print("\nPress enter to continue")
    input()
    

if __name__ == "__main__":
    main()