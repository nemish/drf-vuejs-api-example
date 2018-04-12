<template>
  <div class="field">
      <label v-if='label' class="label">{{label}}</label>
      <div class="control has-icons-left has-icons-right">
        <input class="input is-success" :type="fieldType" :placeholder="placeholder" :name='name' @input='onInput' :value='value' />
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
            value: this.$store.state[this.formName + 'Form'][this.name]
        }
    },
    props: {
        label: {
            type: String
        },
        placeholder: {
            type: String,
            default: ''
        },
        fieldType: {
            type: String,
            default: 'text'
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
        icon: {
            type: String
        }
    },
    methods: {
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
        fieldOk() {
            return !!this.value;
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang='stylus' scoped>
</style>