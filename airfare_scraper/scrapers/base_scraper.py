class BaseScraper:
    """
    Abstract base class for all airfare scrapers.
    Defines the standard interface that all scraper implementations must follow.
    """
    
    def search_fares(self, origin, destination, departure_date):
        """
        Search for fares between origin and destination on a specific date.
        
        Args:
            origin (str): IATA code for the origin airport (e.g., 'DEL')
            destination (str): IATA code for the destination airport (e.g., 'BOM')
            departure_date (str): Date in 'YYYY-MM-DD' format
            
        Returns:
            list: A list of dictionaries representing standard airfare observations.
        """
        raise NotImplementedError("Subclasses must implement the search_fares method.")
