<template>
  <div class="field">
      <label v-if='label' class="label">{{label}}</label>
      <div class="control has-icons-left has-icons-right">
        <div class="select">
          <select v-model='value' @input='onInput'>
            <option value=''> -- select an option -- </option>
            <option v-for='(item, index) in options' :key='item.id' :value='item.id'>{{getTitle(item)}}</option>
          </select>
        </div>
        <span v-if='icon' class="icon is-small is-left">
          <i :class="`fas fa-${icon}`"></i>
        </span>
        <span v-if='fieldOk' class="icon is-small is-right">
          <i class="fas fa-check"></i>
        </span>
      </div>
      <p v-if='statusMessage' :class="`help is-${status}`">{{statusMessage}}</p>
  </div>
</template>

<script>
export default {
    name: 'FormField',
    data() {
        return {
            value: this.$store.state[this.formName + 'Form'][this.name] || ''
        };
    },
    mounted() {
        if (this.loadUrl && !this.options.length) {
            this.$store.dispatch(`${this.formName}Form/loadSelect`, {
                url: this.loadUrl,
                name: this.name
            })
        }
    },
    props: {
        loadUrl: {
            type: String,
            required: true
        },
        label: {
            type: String
        },
        placeholder: {
            type: String,
            default: ''
        },
        status: {
            type: String,
            default: 'success'
        },
        statusMessage: {
            type: String
        },
        name: {
            type: String,
            required: true
        },
        formName: {
            type: String
        },
        displayField: {
            type: String
        },
        icon: {
            type: String
        }
    },
    methods: {
        getTitle(item) {
            return item[this.displayField || 'username'];
        },
        onInput(event) {
            this.value = event.currentTarget.value;
            const {
                name,
                value
            } = this;
            this.$emit('change-value', {
                name,
                value
            });
            if (this.formName) {
                this.$store.dispatch(`${this.formName}Form/changeValue`, {name, value});
            }
        }
    },
    computed: {
        options() {
            const meta = this.$store.state[this.formName + 'Form']._meta[this.name];
            return meta ? meta.options || [] : [];
        },
        isLoading() {
            return this.$store.state[this.formName + 'Form'];
        },
        fieldOk() {
            return !!this.value;
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang='stylus' scoped>
</style>