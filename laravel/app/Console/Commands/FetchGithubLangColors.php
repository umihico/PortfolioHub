<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;

class FetchGithubLangColors extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'command:FetchGithubLangColors';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Download json from https://raw.githubusercontent.com/ozh/github-colors/master/colors.json and update db.';

    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct()
    {
        parent::__construct();
    }

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {

        $url="https://raw.githubusercontent.com/ozh/github-colors/master/colors.json";
        $client = new \GuzzleHttp\Client();
        $response = $client->get($url);
        file_put_contents('./resources/js/colors.js', "color_dict=".$response->getBody());
    }
}
