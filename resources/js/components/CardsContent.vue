<template>
    <div>
        <v-container>
            <v-autocomplete
                v-model="location"
                v-if="locations.length"
                :items="locations"
                @input="push()"
                clearable
                chips
                label="Location filter"
                solo
            ></v-autocomplete>
        </v-container>
        <div class="text-center">
            <pagination :page="parseInt(page)" @pageHandler='set_page' ref="header_pagination"></pagination>
        </div>
        <v-row no-gutters>
            <template v-for="i in 12">
                <v-col :key="i" cols="12" sm="12" md="6">
                    <portfolio_card ref="portfolio_card"></portfolio_card>
                </v-col>
            </template>
        </v-row>
        <div class="text-center">
            <pagination :page="parseInt(page)" @pageHandler='set_page' ref="footer_pagination"></pagination>
        </div>
    </div>
</template>
<script>

    let load_portfolio = function (app) {
        let query = {page: parseInt(app.page), location: app.location};
        axios.post(`/api/fetch_portfolio_ids?_=${new Date().getTime()}`, query).then(function (res) {

            console.log(res.data);
            if (res.data.data.length == 0 && app.page > 1) {
                app.page = res.data.last_page;
                app.push();
            }
            app.set_portfolios(res.data);
        }).catch(function (error) {
            console.log(error);
        }).finally(function () {
        });
    };
    import portfolio_card from './PortfolioCard.vue';
    import pagination from './pagination.vue';

    export default {
        name: "cards",
        components: {
            portfolio_card,
            pagination,
        },
        data() {
            return {
                locations: [],
                location: "",
                value: null,
                page: 1,
            };
        },
        watch: {
            '$route'(to, from) {
                this.page = parseInt(to.query.page); // setting variables when going back
                this.$refs['header_pagination'].data_page = this.page;
                this.$refs['footer_pagination'].data_page = this.page;
                this.location = to.query.location; // setting variables when going back
                load_portfolio(this);
            }
        },
        methods: {
            set_portfolios(data) {
                for (let i = 0; i < 12; i++) {
                    if (i < data.data.length) {
                        this.$refs['portfolio_card'][i].set(data.data[i]);
                    } else {
                        this.$refs['portfolio_card'][i].clear();
                    }
                }
                this.$refs['header_pagination'].show(data.last_page);
                this.$refs['footer_pagination'].show(data.last_page);
            },
            set_page(msg) {
                // receiving message(page) from pagination component
                this.page = msg;
                this.push();
            },
            push() {
                let query = {page: this.page};
                if (this.location) query.location = this.location;
                this.$router.push({path: "/", query: query});
                window.history.replaceState({}, '', "/?" + Object.keys(query).map(key => `${key}=${encodeURIComponent(query[key])}`).join('&'));
            }
        },
        created() {
            this.location = this.$route.query.location;
            this.page = (this.$route.query.page) ? parseInt(this.$route.query.page) : 1;
            load_portfolio(this);
            let app = this;
            axios.get(`/api/fetch_geotags?_=${new Date().getTime()}`).then(function (res) {
                app.locations = res.data;
            }).catch(function (error) {
                console.log(error);
            }).finally(function () {
            });
        }
    };
</script>
