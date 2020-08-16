<template>
    <transition name="fade" mode="out-in">
        <v-card
            @mouseenter="hovered=true"
            @mouseleave="hovered=false"
            class="ma-4"
            v-if="gif"
        >
            <a :href="'https://github.com/'+user" target="_blank" style="color: inherit; text-decoration: none;">
                <v-card-title class="font-weight-black">
                    <v-avatar size="50px" class="ma-1" v-if="user">
                        <img
                            :src="'https://avatars.githubusercontent.com/'+user+'?s=50'"
                        >
                    </v-avatar>
                    {{ user }}
                </v-card-title>
            </a>
            <a target="_blank" :href="url" :key="gif">
                <v-img
                    class="white--text align-end"
                    width="100%"
                    :src="gif"
                >
                </v-img>
            </a>
            <v-card-text class="text--primary">
                <div class="" style="display: flex;">
                    <template v-for="(ratio,lang) in skills">
                        <p class="color-bar"
                           :style="'height: 7px;background-color: '+String((color_dict[lang]) ? color_dict[lang].color : 'red')+'; width: '+ratio+'%'"></p>
                    </template>
                </div>
                <template v-for="(ratio,lang) in skills" v-if="hovered">
                    <span style="display: inline-block;"><span
                        :style="'background-color: '+String((color_dict[lang]) ? color_dict[lang].color : 'red')+';color: '+String((color_dict[lang]) ? color_dict[lang].color : 'red')+';border-radius: 100px;'">・</span><span
                        class="mr-2 ml-1">{{lang}}</span></span>
                </template>
                <v-row>
                    <v-col cols="8">
                        <v-icon>mdi-map-marker</v-icon>
                        {{ raw_location }}
                    </v-col>
                    <v-col cols="4">
                        <v-icon>mdi-star</v-icon>
                        {{ stars }}
                    </v-col>
                    <v-col cols="8">
                        <a :href="'https://github.com/'+user+'/'+repository" target="_blank"
                           style="color: inherit; text-decoration: none;">
                            <v-icon>mdi-github</v-icon>
                            {{ repository }}</a>
                    </v-col>
                    <v-col cols="4">
                        <v-icon>mdi-source-fork</v-icon>
                        {{ forks }}
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>
    </transition>
</template>

<script>
    export default {
        name: "portfolio_card",
        data() {
            return {
                hovered: false,
                gif: "",
                url: "",
                user: '',
                repository: '',
                raw_location: "",
                stars: "",
                forks: "",
                skills: [],
                color_dict: color_dict,
            };
        },
        methods: {
            clear() {
                this.url = "";
                this.gif = "";
                this.user = '';
                this.repository = '';
                this.raw_location = "";
                this.stars = "";
                this.forks = "";
                this.skills = [];
            },
            set(data) {
                this.gif = "";
                setTimeout(() => {
                    this.url = data.url;
                    this.gif = data.gif;
                    this.user = data.user;
                    this.repository = data.repository;
                    this.raw_location = data.raw_location;
                    this.stars = data.stars;
                    this.forks = data.forks;
                    this.skills = JSON.parse(data.skills);
                }, 300);
            },
        }
    };

</script>
