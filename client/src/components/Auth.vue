<template>
    <div class="container">
      <h1 class="title">
        <router-link :to="{name: 'Login'}">Login</router-link>
        &nbsp;|&nbsp;
        <router-link :to="{name: 'Register'}">Register</router-link>
      </h1>
      <router-view />
    </div>
</template>

<script>
export default {
  name: 'Auth',
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang='stylus' scoped>

.container {
    max-width 500px
}
</style>