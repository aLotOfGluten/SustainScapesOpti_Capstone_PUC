import src.solve_parallelized 
import src.join_and_local_search
from config.config_run_all import localsearch

def main():
    src.solve_parallelized.main()
    if localsearch:
        src.join_and_local_search.main()

if __name__ == '__main__':
    main()