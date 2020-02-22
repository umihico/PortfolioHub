<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('spa');
});

Route::any('/{any}', function (\Illuminate\Http\Request $request) {
    if(file_exists(public_path($request->path()))){
        return response()->file(public_path($request->path()));
    }else{
        return redirect('/');
    }
})->where('any', '.*');
