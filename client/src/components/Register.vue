<template>
    <h3>The work in progress...</h3>
</template>

<script>
import {
    mapState
} from 'vuex';
import FormField from '@/components/FormField';

const REQUIRED_FIELDS = [
    'username',
    'password',
    'password2',
    'email'
]

export default {
  name: 'Register',
  components: {
    field: FormField
  },
  computed: {
    ...mapState({
        data: state => state.registerForm,
        user: state => state.user
    }),
    submitDisallowed() {
        if (this.user.loading) {
            return true;
        }
        return REQUIRED_FIELDS.some(field => !this.data[field]) || this.data.password !== this.data.password2;
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang='stylus' scoped>
</style>