var app = angular.module('nlApp', []);
app.controller('nlCtrl', function($scope, $http) {
	NUMBER_OF_MONTHS = 9;

	$scope.selectedArticle = {};
	$scope.monthList = [];
	for (var i = 0; i < NUMBER_OF_MONTHS; i++) {
		$scope.monthList.push({
			'label': 'Month ' + (i + 1),
			'id': (i + 1)
		});
	}

	$scope.sidebarClick = function(id) {
		$http.get("/api/postbirth_articles/" + id).then(function(response) {
			$scope.selectedArticle = response.data.data;
			console.log(response.data.data);
		});
	}

	$scope.sidebarClick(1);

	console.log($scope.monthList);
});