from get_info import Queries
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('-s', '--sex', help='Sex')
parser.add_argument('-m', '--method', help='Method')
parser.add_argument('-y', '--year', help='Year')
parser.add_argument('-t', '--territory', help='Territory')
parser.add_argument('-n', '--next_territory', help='Next_Territory')

args = parser.parse_args()

if args.method == 'przystępowalność':
    if (args.sex == 'kobiety') or (args.sex == 'mężczyźni'):
        Queries('database.db').queryset_mean(sex=args.sex, territory=args.territory, year=args.year)
    elif args.sex is None:
        Queries('database.db').queryset_mean(territory=args.territory, year=args.year)

elif args.method == 'zdawalność':
    if (args.sex == 'kobiety') or (args.sex == 'mężczyźni'):
        Queries('database.db').queryset_percentage_pass_rate(sex=args.sex, territory=args.territory)
    elif args.sex is None:
        Queries('database.db').queryset_percentage_pass_rate(territory=args.territory)

elif args.method == 'najlepsze':
    if (args.sex == 'kobiety') or (args.sex == 'mężczyźni'):
        Queries('database.db').queryset_the_best_pass_ratio(sex=args.sex, year=args.year)
    elif args.sex is None:
        Queries('database.db').queryset_the_best_pass_ratio(year=args.year)

elif args.method == 'lepsze':
    if (args.sex == 'kobiety') or (args.sex == 'mężczyźni'):
        Queries('database.db').queryset_better_territory(sex=args.sex,
                                                         territory1=args.territory,
                                                         territory2=args.next_territory)
    else:
        Queries('database.db').queryset_better_territory(territory1=args.territory, territory2=args.next_territory)

elif args.method == 'regres':
    if (args.sex == 'kobiety') or (args.sex == 'mężczyźni'):
        Queries('database.db').queryset_regression(sex=args.sex)
    else:
        Queries('database.db').queryset_regression()
else:
    print("Niepoprawna metoda")
