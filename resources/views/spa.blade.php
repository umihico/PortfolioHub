<!doctype html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <link rel="stylesheet" href="{{ asset(mix('css/app.css')) }}">
    <link href="https://fonts.googleapis.com/css?family=Nunito:200,600" rel="stylesheet" type="text/css">
    <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900|Material+Icons"
          rel="stylesheet"/>
    <title>PortfolioHub</title>
</head>
<body>
<v-app id="app">
    <v-content>
        <v-container>
            <div class="display-4">PortfolioHub</div>
            <a class="github-button" href="https://github.com/umihico" data-size="large" data-show-count="true"
               aria-label="Follow @umihico on GitHub">Follow @umihico</a>
            <a class="github-button" href="https://github.com/umihico/PortfolioHub" data-icon="octicon-star"
               data-size="large" data-show-count="true" aria-label="Star umihico/PortfolioHub on GitHub">Star</a>
            <a class="github-button" href="https://github.com/umihico/PortfolioHub/issues"
               data-icon="octicon-issue-opened" data-size="large" data-show-count="true"
               aria-label="Issue umihico/PortfolioHub on GitHub">Issue</a>
            <router-view ref="cards_content"></router-view>
        </v-container>
    </v-content>
</v-app>
<script src="https://buttons.github.io/buttons.js"></script>
<script src="{{ asset(mix('js/app.js')) }}"></script>
<style>
    .fade-leave-active, .fade-enter-active {
        transition: opacity 0.5s;
    }

    .fade-enter,
    .fade-leave-to {
        opacity: 0;
    }
</style>
</body>
</html>
