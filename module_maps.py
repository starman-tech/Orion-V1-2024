from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests


class LocalSearch:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="local_search_app")

    def find_nearby_places(self, query, location, max_results=10, radius_km=5):
        """
        Trouve des lieux à proximité basés sur une recherche textuelle.

        :param query: Type de lieu à chercher (ex: 'pizzeria').
        :param location: Coordonnées de départ sous forme (latitude, longitude).
        :param max_results: Nombre maximal de résultats à renvoyer.
        :param radius_km: Rayon de recherche en kilomètres.
        :return: Liste des lieux trouvés avec nom et coordonnées.
        """
        search_results = []
        places = self.geolocator.geocode(query, exactly_one=False)

        if not places:
            return []

        for place in places:
            place_coords = (place.latitude, place.longitude)
            distance = geodesic(location, place_coords).kilometers
            if distance <= radius_km:
                search_results.append({
                    'name': place.address,
                    'coordinates': place_coords,
                    'distance_km': round(distance, 200)
                })

        search_results = sorted(search_results, key=lambda x: x['distance_km'])
        return search_results[:max_results]

    def get_route(self, start_coords, destination_coords):
        """
        Calcule un itinéraire entre deux points en utilisant OSRM API.

        :param start_coords: Coordonnées de départ sous forme (latitude, longitude).
        :param destination_coords: Coordonnées de destination sous forme (latitude, longitude).
        :return: Détails de l'itinéraire (distance, durée, étapes).
        """
        base_url = "http://router.project-osrm.org/route/v1/driving/"
        coords = f"{start_coords[1]},{start_coords[0]};{destination_coords[1]},{destination_coords[0]}"
        response = requests.get(f"{base_url}{coords}?overview=false")

        if response.status_code != 200:
            return None

        route_data = response.json()
        if not route_data.get("routes"):
            return None

        route = route_data["routes"][0]
        return {
            "distance_km": route["distance"] / 1000,
            "duration_min": route["duration"] / 60,
            "steps": route.get("legs", [])[0].get("steps", [])
        }
