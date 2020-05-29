<?php

namespace App\Http\Controllers;

use App\Portfolio;
use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Storage;
use Validator;

class PortfolioController extends Controller
{
    public function fetch_geotags(Request $request)
    {
        $locations = [];
        foreach (DB::table('portfolios')->distinct()->select(['id', 'locations'])->whereNotNull('gif')->whereNotNull('locations')->get()->toArray() as $record) {
            foreach (json_decode($record->locations, true) as $location) {
                if (strlen($location) == 0) continue;
                if (!array_key_exists($location, $locations)) $locations[$location] = 0;
                $locations[$location] += 1;
            }
        }
        arsort($locations);
        $locations = array_map(function ($count, $location) {
            return "($count)$location";
        }, array_values($locations), array_keys($locations));
        return $locations;
    }

    public function fetch_portfolio_ids(Request $request)
    {
        Validator::make($request->all(), [
            "page" => 'nullable|integer',
            "sort" => 'nullable|string|in:stars,forks',
            "filter" => 'nullable|string',
        ])->validate();
        $query = DB::table('portfolios')
            ->whereNotNull('gif')
            ->orderByDesc($request->get('sort', 'stars'));
        $location = $request->get('location', false);
        if ($location) {
            $location = explode(')', $location)[1];
            $query = $query->whereJsonContains('locations', $location);
        }
        $paginated = $query->paginate(12);
        $array = $paginated->toArray();
        foreach ($array['data'] as $r => $record) {
            $array['data'][$r]->gif = Storage::disk('s3')->temporaryUrl($record->gif, Carbon::now()->addDays(7));
        }
        return $array;
    }
}
