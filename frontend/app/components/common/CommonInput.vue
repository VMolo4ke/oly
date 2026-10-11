<template>
  <label class="ui-input">
    <span v-if="label" class="ui-input__label">{{ label }}</span>
    <input
      v-model="model"
      class="ui-input__field"
      :type="type"
      :placeholder="placeholder"
      :autocomplete="autocomplete"
      :required="required"
      :minlength="minlength"
      :maxlength="maxlength"
    >
  </label>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  label?: string
  type?: string
  placeholder?: string
  autocomplete?: string
  required?: boolean
  minlength?: number
  maxlength?: number
}>(), {
  type: 'text',
  label: undefined,
  placeholder: undefined,
  autocomplete: undefined,
  minlength: undefined,
  maxlength: undefined
})

const model = defineModel<string>({ default: '' })
</script>

<style lang="scss" scoped>
.ui-input {
  display: flex;
  flex-direction: column;
  gap: 6px;

  &__label {
    font-size: 14px;
    color: $text-muted;
  }

  &__field {
    padding: 12px 14px;
    color: $text;
    background: $surface;
    border: 1px solid $border;
    border-radius: 10px;
    outline: none;
    transition: border-color 0.15s, box-shadow 0.15s;

    &::placeholder {
      color: rgba($text-muted, 0.65);
    }

    &:focus {
      border-color: $green-400;
      box-shadow: 0 0 0 3px rgba($green-400, 0.25);
    }
  }
}
</style>