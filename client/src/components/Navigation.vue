<template>
    <nav class="level padding-vert-md padding-hor-md">
      <div class="level-left">
        <div class="level-item" v-if='loggedIn'>
          <h1 class="subtitle is-5">
            <router-link to='/shipments'>Shipments</router-link>
          </h1>
        </div>
      </div>
      <div class="level-right" v-if='loggedIn'>
        <div class="level-item">
            <p class="control margin-sides-10">{{user.username}}</p>
            <p class="control">
              <button class="button is-primary" @click='exit'>Exit</button>
            </p>
        </div>
      </div>
    </nav>
</template>

<script>
import {
    mapState,
    mapGetters,
    mapActions
} from 'vuex';

export default {
  name: 'Navigation',
  data () {
    return {};
  },
  methods: {
    ...mapActions('user', ['logout']),
    exit() {
        this.logout().then(() => {
            this.$router.push({name: 'Login'});
        })
    }
  },
  computed: {
    ...mapState({
        user: state => state.user.data
    }),
    ...mapGetters('user', ['loggedIn'])
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
