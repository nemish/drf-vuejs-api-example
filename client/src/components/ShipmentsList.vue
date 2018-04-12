<template>
    <table class="table">
        <thead>
          <tr>
            <th>Client</th>
            <th>From city</th>
            <th>From street</th>
            <th>From address</th>
            <th>Recipient</th>
            <th>To city</th>
            <th>To street</th>
            <th>To address</th>
            <th>Deadline</th>
            <th>Weight</th>
            <th></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
            <tr v-for='(item, index) in shipments.data' :key='item.id'>
                <td>{{item.client.username}}</td>
                <td>{{item.from_city.name}}</td>
                <td>{{item.from_street.name}}</td>
                <td>{{item.from_address}}</td>
                <td>{{item.recipient.username}}</td>
                <td>{{item.dest_city.name}}</td>
                <td>{{item.dest_street.name}}</td>
                <td>{{item.dest_address}}</td>
                <td>{{formatDeadline(item.deadline)}}</td>
                <td>{{getWeight(item)}}</td>
                <td>
                    <a class='button' @click='editShipment(item)'>
                        <span class="icon is-small">
                            <i class="fas fa-edit"></i>
                        </span>
                    </a>
                </td>
                <td>
                    <a class='button' @click='doDeleteShipment(item)'>
                        <span class="icon is-small">
                            <i class="fas fa-trash"></i>
                        </span>
                    </a>
                </td>
            </tr>
        </tbody>
    </table>
</template>

<script>
import {
    mapActions,
    mapState,
    mapGetters
} from 'vuex';

export default {
  name: 'ShipmentsList',
  mounted() {
    if (!this.loggedIn) {
        this.$router.push({name: 'Home'});
        return;
    }
    this.fetchItems();
  },
  methods: {
    ...mapActions('shipments', ['fetchList', 'deleteShipment']),
    ...mapActions('shipmentForm', ['initFormValues']),
    fetchItems() {
        const params = {};
        if (this.$route.query.filter !== 'all') {
            params.client_id = this.user.id;
        }
        this.fetchList(params);
    },
    editShipment(item) {
        const data = {...item};
        Object.keys(item).forEach(key => {
            const inner = item[key];
            if (inner && inner.id) {
                data[key + '_id'] = inner.id;
            }
        });
        if (data.deadline) {
            data.deadline = data.deadline.split('T')[0];
        }
        this.initFormValues(data).then(() => {
            this.$router.push({name: 'EditShipment', params: {id: item.id}});
        });
    },
    doDeleteShipment(item) {
        const { id } = item;
        this.deleteShipment({ id }).then(() => {
            this.fetchItems();
        });
    },
    formatDeadline(dateStr) {
        if (!dateStr) {
            return
        }

        const dt = new Date(dateStr);
        return dt.toLocaleDateString();
    },
    getWeight(item) {
        if (!item.weight) {
            return
        }
        return `${item.weight}kg`;
    }
  },
  computed: {
    ...mapState({
        loading: state => state.shipments.loading,
        shipments: state => state.shipments,
        user: state => state.user.data
    }),
    ...mapGetters('user', ['loggedIn']),
    showAll() {
        return this.$route.query.filter === 'all';
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>