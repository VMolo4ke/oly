<template>
  <button
    class="ui-button"
    :class="`ui-button--${variant}`"
    :type="type"
    :disabled="disabled || loading"
  >
    <span v-if="loading" class="ui-button__spinner" />
    <slot />
  </button>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  type?: 'button' | 'submit'
  variant?: 'primary' | 'ghost'
  disabled?: boolean
  loading?: boolean
}>(), {
  type: 'button',
  variant: 'primary'
})
</script>

<style lang="scss" scoped>
.ui-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 18px;
  color: $text-on-accent;
  cursor: pointer;
  border: 1px solid transparent;
  border-radius: 10px;
  transition: background 0.15s, opacity 0.15s;

  &--primary {
    background: $green-600;

    &:hover:not(:disabled) {
      background: $green-700;
    }
  }

  &--ghost {
    color: $green-700;
    background: transparent;
    border-color: $border-strong;

    &:hover:not(:disabled) {
      background: $green-100;
    }
  }

  &:disabled {
    cursor: not-allowed;
    opacity: 0.55;
  }

  &__spinner {
    width: 14px;
    height: 14px;
    border: 2px solid currentcolor;
    border-top-color: transparent;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
