import random
from django.shortcuts import render
from django.views import View
from data import mock_data


class Data:
    tours = mock_data.tours
    title = mock_data.title
    subtitle = mock_data.subtitle
    description = mock_data.description
    departures = mock_data.departures


class MainView(View):

    @staticmethod
    def get_tours(tours):
        keys = list(tours.keys())
        random.shuffle(keys)
        main_tours = {}
        for i in range(1, 7):
            main_tours[i] = Data.tours.get(keys[i])

        return main_tours

    def get(self, request):
        flight_from = ''
        global_pic = Data.tours.get(7).get('picture')
        main_tours = self.get_tours(Data.tours)

        return render(request, 'tours/index.html',
                      {'tours': main_tours, 'title': Data.title,
                       'departures': Data.departures, 'flight_from': flight_from,
                       'subtitle': Data.subtitle, 'description': Data.description,
                       'global_pic': global_pic})


class DepView(View):

    @staticmethod
    def get_tours(departure, all_tours):
        cur_tours = {}
        for key, value in all_tours.items():
            if value['departure'] == departure:
                cur_tours[key] = value

        return cur_tours

    @staticmethod
    def get_tours_params(cur_tours):

        min_price_key = min(cur_tours, key=lambda k: cur_tours[k]['price'])
        max_price_key = max(cur_tours, key=lambda k: cur_tours[k]['price'])

        min_night_key = min(cur_tours, key=lambda k: cur_tours[k]['nights'])
        max_night_key = max(cur_tours, key=lambda k: cur_tours[k]['nights'])

        return {'min_price': cur_tours[min_price_key]['price'], 'max_price': cur_tours[max_price_key]['price'],
                'min_night': cur_tours[min_night_key]['nights'], 'max_night': cur_tours[max_night_key]['nights']}

    def get(self, request, departure):

        cur_tours = self.get_tours(departure, Data.tours)
        flight_from = Data.departures.get(departure)
        param_tours = self.get_tours_params(cur_tours)

        return render(request, 'tours/departure.html',
                      {'tours': cur_tours, 'title': Data.title, 'departures': Data.departures,
                       'flight_from': flight_from, 'param_tours': param_tours})


class TourView(View):

    @staticmethod
    def get_starts(cur_tour):
        return int(cur_tour.get('stars')) * '★'

    def get(self, request, tour_id):
        cur_tour = mock_data.tours.get(tour_id)
        flight_from = Data.departures.get(cur_tour.get('departure'))
        stars = self.get_starts(cur_tour)

        return render(request, 'tours/tour.html',
                      {'tours': cur_tour, 'title': Data.title, 'departures': Data.departures,
                       'flight_from': flight_from, 'stars': stars})
