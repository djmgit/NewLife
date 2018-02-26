var app = angular.module('nlApp', []);
app.controller('nlCtrl', function($scope, $http) {
	$scope.selectedArticle = null;
	$scope.articles = []

	$scope.sidebarClick = function(id) {
		$http.get("/api/blogs/get_blog/" + id).then(function(response) {
			$scope.selectedArticle = response.data.data;
			$(".article-body").html(response.data.data.article);
			console.log(response.data.data.article);
		});
	}

	// get artcle titles and ids

	$http.get('/api/blogs/blog_titles').then(function(response) {
		$scope.articles = response.data.data.reverse();
		$scope.sidebarClick($scope.articles[0].id);
	});
});