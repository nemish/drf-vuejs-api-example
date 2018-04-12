<template>
    <form>
      <p v-if='user.errors.length'>{{user.errors[0]}}</p>
      <field label="Username" name="username" placeholder="6 or more characters" icon="user" formName='login' />
      <field label="Password" name="password" fieldType='password' placeholder="something secret" icon="lock" formName='login' />
      <div class="control">
        <button :class="btnClass" :disabled='submitDisallowed' @click.stop.prevent='submit'>Submit</button>
      </div>
    </form>
</template>

<script>
import {
    mapState,
    mapGetters,
    mapActions
} from 'vuex';
import FormField from '@/components/FormField';

export default {
  name: 'Login',
  components: {
    field: FormField
  },
  computed: {
    ...mapState({
        data: state => state.loginForm,
        user: state => state.user
    }),
    submitDisallowed() {
        return this.user.loading || !this.data.username || !this.data.password;
    },
    btnClass() {
        return ['button', 'is-link', this.user.loading ? 'is-loading' : null];
    }
  },
  methods: {
    ...mapActions('user', ['login']),
    submit() {
        const {
            username,
            password
        } = this.data;
        return this.login({username, password}).then(() => {
            this.$router.push({name: 'ShipmentsList'});
        });
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang='stylus' scoped>
</style>