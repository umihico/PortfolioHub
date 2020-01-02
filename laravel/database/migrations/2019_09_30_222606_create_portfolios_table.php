<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreatePortfoliosTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('portfoliohub', function (Blueprint $table) {
            $table->bigInteger('id')->primary();
            $table->string('user');
            $table->string('repository');
            $table->dateTime('repository_updated_at');
            $table->integer('stars');
            $table->integer('forks');
            $table->string('url')->nullable();
            $table->dateTime('api_fetched_at');
            $table->string('gif')->nullable();
            $table->dateTime('gif_updated_at')->nullable();
            $table->string('raw_location')->nullable();
            $table->json('locations')->nullable();
            $table->dateTime('locations_updated_at')->nullable();
            $table->json('skills')->nullable();
            $table->dateTime('skills_updated_at')->nullable();
            $table->string('error_detail')->nullable();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('portfoliohub');
    }
}
