function create_query(lon, lat) {
	return 'http://api.openweathermap.org/data/2.5/forecast/daily?' +
	  'lat=' + lon +
	 '&lon=' + lat +
	 '&mode=json' +
	 '&units=metric' +
	 '&cnt=7' +
	 '&appid=' + get_owm_api_key();
};
