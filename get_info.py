import sqlite3


class Queries:

    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def queryset_mean(self, territory, year, sex='wszyscy'):
        if sex == 'kobiety' or sex == 'mężczyźni':
            divider = 1
            data = self.cursor.execute(f'SELECT Rok, Liczba_osób FROM MATURITY_EXAM WHERE '
                                       f'Płeć="{sex}" '
                                       f'AND Terytorium = "{territory}"'
                                       f'AND Przystąpiło_zdało = "przystąpiło"'
                                       f'AND Rok BETWEEN 2010 AND {year}')
        else:
            divider = 2
            data = self.cursor.execute(f'SELECT Rok, Liczba_osób FROM MATURITY_EXAM WHERE '
                                       f'Terytorium = "{territory}"'
                                       f'AND Przystąpiło_zdało = "przystąpiło"'
                                       f'AND Rok BETWEEN 2010 AND {year}')
        how_many_years = 0
        how_many_persons = 0
        for record in data:
            how_many_years += 1
            how_many_persons += record[1]
        mean = how_many_persons // (how_many_years // divider)
        print(f"{year}  -   {mean}")
        self.connection.close()

    def queryset_percentage_pass_rate(self, territory,  sex='wszyscy'):
        acceded_matches = []
        passed_matches = []
        if sex == 'kobiety' or sex == 'mężczyźni':
            data = self.cursor.execute(f'SELECT Rok, Przystąpiło_zdało, Liczba_osób FROM MATURITY_EXAM WHERE '
                                       f'Płeć="{sex}" '
                                       f'AND Terytorium = "{territory}"')
            for record in data:
                if record[1] == 'przystąpiło':
                    acceded_matches.append(record)
                else:
                    passed_matches.append(record)

            for passed_match, acceded_match in zip(passed_matches, acceded_matches):
                print(f'{passed_match[0]}   -   {round(passed_match[2] / acceded_match[2] * 100, 2)}%')

            self.connection.close()

        else:

            data = self.cursor.execute(f'SELECT Rok, Przystąpiło_zdało, Liczba_osób FROM MATURITY_EXAM WHERE '
                                       f'Terytorium = "{territory}"')
            for record in data:
                if record[1] == 'przystąpiło':
                    acceded_matches.append(record)
                else:
                    passed_matches.append(record)

            even_acceded_records = []
            even_passed_records = []
            odd_acceded_records = []
            odd_passed_records = []

            for i, (passed_match, acceded_match) in enumerate(zip(passed_matches, acceded_matches)):
                if i % 2 == 0:
                    even_acceded_records.append(acceded_match)
                    even_passed_records.append(passed_match)
                else:
                    odd_acceded_records.append(acceded_match)
                    odd_passed_records.append(passed_match)

            for even_acceded_record, even_passed_record, odd_acceded_record, odd_passed_record\
                    in zip(even_acceded_records, even_passed_records, odd_acceded_records, odd_passed_records):
                acceded_nr = even_acceded_record[2] + odd_acceded_record[2]
                passed_nr = even_passed_record[2] + odd_passed_record[2]
                print(f'{even_passed_record[0]}   -   {round(passed_nr / acceded_nr * 100, 2)}%')
            self.connection.close()

    def queryset_the_best_pass_ratio(self, year, sex='wszyscy'):
        all_territories = []
        acceded_matches = []
        passed_matches = []

        if sex == 'kobiety' or sex == 'mężczyźni':
            data = self.cursor.execute(f'SELECT Rok, Przystąpiło_zdało, Liczba_osób, Terytorium FROM MATURITY_EXAM '
                                       f'WHERE Płeć="{sex}" '
                                       f'AND Rok = {year}')
            for record in data:
                if record[1] == 'przystąpiło':
                    acceded_matches.append(record[2])
                    all_territories.append(record[3])
                else:
                    passed_matches.append(record[2])
            pass_ratio = []

            for passed_match, acceded_match in zip(passed_matches, acceded_matches):
                pass_ratio.append(round(passed_match / acceded_match * 100, 2))
            max_ratio = max(pass_ratio)

            for i, current_ratio in enumerate(pass_ratio):
                if max_ratio == current_ratio:
                    best_territory = all_territories[i]
                    max_ratio = current_ratio
                    break
            print(f"{best_territory}    -   {max_ratio}%")
            self.connection.close()

        else:

            data = self.cursor.execute(f'SELECT Rok, Przystąpiło_zdało, Liczba_osób, Terytorium FROM MATURITY_EXAM'
                                       f' WHERE Rok = {year}')

            for record in data:
                if record[1] == 'przystąpiło':
                    acceded_matches.append(record[2])
                    if record[3] not in all_territories:
                        all_territories.append(record[3])
                else:
                    passed_matches.append(record[2])

            even_acceded_records = []
            even_passed_records = []
            odd_acceded_records = []
            odd_passed_records = []
            
            for i, (passed_match, acceded_match) in enumerate(zip(passed_matches, acceded_matches)):
                if i % 2 == 0:
                    even_acceded_records.append(acceded_match)
                    even_passed_records.append(passed_match)
                else:
                    odd_acceded_records.append(acceded_match)
                    odd_passed_records.append(passed_match)

            pass_ratio = []

            for i, (even_acceded_record, even_passed_record, odd_acceded_record, odd_passed_record)\
                    in enumerate\
                        (zip(even_acceded_records, even_passed_records, odd_acceded_records, odd_passed_records)):
                acceded_nr = even_acceded_record + odd_acceded_record
                passed_nr = even_passed_record + odd_passed_record
                pass_ratio.append(round(passed_nr / acceded_nr * 100, 2))
            max_ratio = max(pass_ratio)

            for i, current_ratio in enumerate(pass_ratio):
                if max_ratio == current_ratio:
                    best_territory = all_territories[i]
                    max_ratio = current_ratio
                    break

            print(f"{best_territory}    -   {max_ratio}%")
            self.connection.close()

    def queryset_better_territory(self, territory1, territory2, sex='wszyscy'):

        territory1_acceded_records = []
        territory1_passed_records = []
        territory2_acceded_records = []
        territory2_passed_records = []
        all_years = []
        ratio_territory1 = []
        ratio_territory2 = []

        if sex == 'kobiety' or sex == 'mężczyźni':
            data = self.cursor.execute(f'SELECT Rok, Przystąpiło_zdało, Liczba_osób, Terytorium '
                                                 f'FROM MATURITY_EXAM WHERE '
                                                 f'Płeć="{sex}" '
                                                 f'AND Terytorium = "{territory1}" OR Terytorium = "{territory2}"')

            for record in data:
                if record[3] == territory1 and record[1] == 'przystąpiło':
                    territory1_acceded_records.append(record[2])
                    all_years.append(record[0])
                elif record[3] == territory1 and record[1] == 'zdało':
                    territory1_passed_records.append(record[2])
                elif record[3] == territory2 and record[1] == 'przystąpiło':
                    territory2_acceded_records.append(record[2])
                elif record[3] == territory2 and record[1] == 'zdało':
                    territory2_passed_records.append(record[2])

            for i in range(len(territory1_acceded_records)):
                ratio_territory1.append(round(territory1_passed_records[i] / territory1_acceded_records[i] * 100, 2))
                ratio_territory2.append(round(territory2_passed_records[i] / territory2_acceded_records[i] * 100, 2))

                if ratio_territory1[i] > ratio_territory2[i]:
                    print(f'{all_years[i]}:     {territory1}')

                elif ratio_territory2[i] > ratio_territory1[i]:
                    print(f'{all_years[i]}:     {territory2}')

                else:
                    print(f'{all_years[i]}:     taka sama zdawalność')

            self.connection.close()

        else:

            data = self.cursor.execute(f'SELECT Rok, Przystąpiło_zdało, Liczba_osób, Terytorium '
                                       f'FROM MATURITY_EXAM WHERE '
                                       f'Terytorium = "{territory1}" OR Terytorium = "{territory2}"')

            for record in data:
                if record[3] == territory1 and record[1] == 'przystąpiło':
                    territory1_acceded_records.append(record[2])
                    all_years.append(record[0])

                elif record[3] == territory1 and record[1] == 'zdało':
                    territory1_passed_records.append(record[2])

                elif record[3] == territory2 and record[1] == 'przystąpiło':
                    territory2_acceded_records.append(record[2])

                elif record[3] == territory2 and record[1] == 'zdało':
                    territory2_passed_records.append(record[2])

            for i in range(0, len(territory1_acceded_records), 2):
                ratio_territory1.append(round(((territory1_passed_records[i] + territory1_passed_records[i + 1]) /
                                              (territory1_acceded_records[i] + territory1_acceded_records[i + 1])) * 100, 2))
                ratio_territory2.append(round(((territory2_passed_records[i] + territory2_passed_records[i + 1]) /
                                              (territory2_acceded_records[i] + territory2_acceded_records[i + 1])) * 100, 2))

            for i in range(len(ratio_territory1)):

                if ratio_territory1[i] > ratio_territory2[i]:
                    print(f'{all_years[i * 2]}:     {territory1}')

                elif ratio_territory2[i] > ratio_territory1[i]:
                    print(f'{all_years[i * 2]}:     {territory2}')

                else:
                    print(f'{all_years[i * 2]}:     taka sama zdawalność')

    def queryset_regression(self, sex='wszyscy'):
        all_territories = []
        all_years = []
        acceded_list = []
        passed_list = []
        ratio_for_current_territory = []

        if sex == 'kobiety' or sex == 'mężczyźni':
            data = self.cursor.execute(f'SELECT Rok, Liczba_osób, Terytorium, Przystąpiło_zdało FROM MATURITY_EXAM WHERE '
                                       f'Płeć="{sex}"'
                                       f'AND Terytorium != "Polska"')
            for record in data:
                if record[2] not in all_territories:
                    all_territories.append(record[2])
                if record[0] not in all_years:
                    all_years.append(record[0])

            for territory in all_territories:

                data = self.cursor.execute(
                    f'SELECT Rok, Liczba_osób, Terytorium, Przystąpiło_zdało FROM MATURITY_EXAM WHERE '
                    f'Płeć="{sex}"'
                    f'AND Terytorium != "Polska"')

                for record in data:

                    if (record[2] == territory) and (record[3] == 'przystąpiło'):
                        acceded_list.append(record[1])

                    elif (record[2] == territory) and (record[3] == 'zdało'):
                        passed_list.append(record[1])

                for acceded, passed in zip(acceded_list, passed_list):
                    ratio_for_current_territory.append(round(passed / acceded * 100, 2))

                for i in range(1, len(ratio_for_current_territory)):

                    if ratio_for_current_territory[i] < ratio_for_current_territory[i - 1]:
                        print(f"{all_years[i - 1]}->{all_years[i]}  - {territory}")

                passed_list.clear()
                acceded_list.clear()
                ratio_for_current_territory.clear()

            self.connection.close()

        else:

            data = self.cursor.execute(
                f'SELECT Rok, Liczba_osób, Terytorium, Przystąpiło_zdało FROM MATURITY_EXAM WHERE '
                f'Terytorium != "Polska"')

            for record in data:
                if record[2] not in all_territories:
                    all_territories.append(record[2])
                if record[0] not in all_years:
                    all_years.append(record[0])

            for territory in all_territories:

                data = self.cursor.execute(
                    f'SELECT Rok, Liczba_osób, Terytorium, Przystąpiło_zdało FROM MATURITY_EXAM WHERE '
                    f'Terytorium != "Polska"')

                for i, record in enumerate(data):

                    if i % 2 == 0:

                        if (record[2] == territory) and (record[3] == 'przystąpiło'):
                            acceded_list.append(record[1])

                        elif (record[2] == territory) and (record[3] == 'zdało'):
                            passed_list.append(record[1])

                    else:

                        if (record[2] == territory) and (record[3] == 'przystąpiło'):
                            acceded_list[len(acceded_list) - 1] += record[1]

                        elif (record[2] == territory) and (record[3] == 'zdało'):
                            passed_list[len(passed_list) - 1] += record[1]

                for acceded, passed in zip(acceded_list, passed_list):
                    ratio_for_current_territory.append(round(passed / acceded * 100, 2))

                for i in range(1, len(ratio_for_current_territory)):

                    if ratio_for_current_territory[i] < ratio_for_current_territory[i - 1]:
                        print(f"{all_years[i - 1]}->{all_years[i]}  - {territory}")

                passed_list.clear()
                acceded_list.clear()
                ratio_for_current_territory.clear()

            self.connection.close()
