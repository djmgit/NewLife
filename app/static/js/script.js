var app = angular.module('nlApp', []);
app.controller('nlCtrl', function($scope, $http) {
	NUMBER_OF_MONTHS = 9;

	$scope.monthList = [];
	for (var i = 0; i < NUMBER_OF_MONTHS; i++) {
		$scope.monthList.push({
			'label': 'Month ' + (i + 1),
			'id': (i + 1)
		});
	}

	$scope.sidebarClick = function(id) {
		$http.get("/api/prebirth_articles/" + id).then(function(response) {
			console.log(response);
		});
	}

	console.log($scope.monthList);
});