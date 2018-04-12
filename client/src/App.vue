<template>
  <div id="app">
    <navigation />
    <router-view />
  </div>
</template>

<script>
import 'bulma/css/bulma.css';
import {
    mapState,
    mapGetters,
    mapActions
} from 'vuex';
import Navigation from '@/components/Navigation';

export default {
  name: 'App',
  components: {
    navigation: Navigation
  },
  mounted() {
    this.handleLogin();
  },
  beforeRouteUpdate() {
    this.handleLogin();
  },
  methods: {
    ...mapActions('user', ['fetchCurrentUser']),
    handleLogin() {
        if (!this.loggedIn && this.$route.name !== 'Login' && this.$route.name !== 'Register') {
            this.fetchCurrentUser().then(() => {
                this.$router.push({path: '/shipments'});
            }).catch(() => {
                this.$router.push({path: '/auth/login'});
            });
        }
    }
  },
  getters: {
    ...mapState({
        user: state => state.user.data
    }),
    ...mapGetters('user', ['loggedIn'])
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Titillium+Web:300');
#app {
  font-family: 'Titillium Web', sans-serif;
}
.padding-vert-lg {
    padding: 20px 0;
}

.padding-vert-md {
    padding-top: 10px;
    padding-bottom: 10px;
}

.padding-hor-md {
    padding-left: 10px;
    padding-right: 10px;
}

.router-link-exact-active {
    color: #363636;
}

.margin-sides-10 {
    margin-left: 10px;
    margin-right: 10px;
}
</style>
