<template>
    <div class="container" v-if='loggedIn'>
        <div class='level'>
            <div class="level-item level-left">
                <p class="control margin-sides-10">Total shipments: {{shipments.total}}</p>
                <p class="control">
                  <button class="button is-primary" @click='toggleNewShipment'>{{newShipmentText}}</button>
                </p>
                <p class="control margin-sides-10" v-if='onList'>
                  <button :class='["button", !isShowAll ? "is-info" : null]' @click='filterMy'>My only</button>
                </p>
                <p class="control" v-if='onList'>
                  <button :class='["button", isShowAll ? "is-info" : null]' @click='filterAll'>All</button>
                </p>
            </div>
        </div>
        <router-view />
    </div>
</template>

<script>
import {
    mapActions,
    mapState,
    mapGetters
} from 'vuex';

export default {
  name: 'Shipments',
  data () {
    return {}
  },
  methods: {
    ...mapActions('shipments', ['fetchList']),
    isInEditMode() {
        return ['NewShipment', 'EditShipment'].indexOf(this.$route.name) > -1;
    },
    toggleNewShipment() {
        const name = this.isInEditMode() ? 'ShipmentsList' : 'NewShipment';
        this.$router.push({name});
    },
    filterMy() {
        this.$router.push({query: {filter: 'my'}});
        this.fetchList({client_id: this.user.id});
    },
    filterAll() {
        this.$router.push({query: {filter: 'all'}});
        this.fetchList();
    }
  },
  computed: {
    ...mapState({
        loading: state => state.shipments.loading,
        user: state => state.user.data,
        shipments: state => state.shipments
    }),
    ...mapGetters('user', ['loggedIn']),
    onList() {
        return this.$route.name === 'ShipmentsList';
    },
    isShowAll() {
        return this.$route.query.filter === 'all';
    },
    newShipmentText() {
        return this.isInEditMode() ? 'Back to list' : 'Create new';
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
