<template>
    <form>
        <p v-if='form._meta.errors.length'>{{form._meta.errors[0]}}</p>
        <div class='field is-horizontal'>
            <div class='field-body'>
              <select-field label="CLient"
                            name="client_id"
                            formName='shipment'
                            loadUrl='/users/?no_page=True' />
              <select-field label="From street"
                            displayField='full_title'
                            name="from_street_id"
                            formName='shipment'
                            loadUrl='/streets/?no_page=True' />
            </div>
        </div>


        <field label="From address" name="from_address" placeholder="house and apartament" icon='address-card' formName='shipment' />

        <div class='field is-horizontal'>
            <div class='field-body'>
              <select-field label="Recipient"
                            name="recipient_id"
                            formName='shipment'
                            loadUrl='/users/?no_page=True' />

              <select-field label="To street"
                            name="dest_street_id"
                            displayField='full_title'
                            formName='shipment'
                            loadUrl='/streets/?no_page=True' />
            </div>
        </div>

      <field label="To address" name="dest_address" placeholder="house and apartament" icon='address-card' formName='shipment' />

      <field label="Deadline" fieldType="date" name="deadline" icon='calendar' formName='shipment' />
      <field label="Weight" name="weight" fieldType='number' placeholder="total weight of shipment" icon='weight' formName='shipment' />
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
import SelectFormField from '@/components/SelectFormField';

const REQUIRED_FIELDS = [
    'client_id',
    'recipient_id',
    'from_street_id',
    'dest_street_id',
];

const OTHER_FIELDS = [
    'from_address',
    'from_city',
    'dest_city',
    'dest_address',
    'deadline',
    'weight'
];


export default {
  name: 'ShipmentForm',
  components: {
    field: FormField,
    'select-field': SelectFormField,
  },
  computed: {
    ...mapState({
        form: state => state.shipmentForm,
        user: state => state.user
    }),
    submitDisallowed() {
        if (this.form._meta.loading) {
            return true;
        }
        return REQUIRED_FIELDS.some(field => !this.form[field]);
    },
    btnClass() {
        return ['button', 'is-link', this.form._meta.loading ? 'is-loading' : null];
    }
  },
  methods: {
    ...mapActions('shipmentForm', [
        'createShipment',
        'updateShipment'
    ]),
    getCityId(streetKey) {
        return this.form._meta[streetKey].options.filter(item => item.id === +this.form[streetKey])[0].city
    },
    submit() {
        const data = {};
        REQUIRED_FIELDS.concat(OTHER_FIELDS).forEach(field => {
            data[field] = this.form[field];
        });
        data.dest_city_id = this.getCityId('dest_street_id');
        data.from_city_id = this.getCityId('from_street_id');
        if (data.deadline) {
            data.deadline += 'T00:00';
        }
        let request;
        if (this.$route.name === 'EditShipment') {
            data.id = this.$route.params.id;
            request = this.updateShipment(data);
        } else {
            request = this.createShipment(data);
        }
        return request.then(() => {
            this.$router.push({name: 'ShipmentsList'});
        });
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang='stylus' scoped>
</style>
