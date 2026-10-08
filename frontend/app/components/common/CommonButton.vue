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
  color: #fff;
  cursor: pointer;
  border: 1px solid transparent;
  border-radius: 10px;
  transition: background 0.15s, opacity 0.15s;

  &--primary {
    background: $royal-violet;

    &:hover:not(:disabled) {
      background: $lavender-purple;
    }
  }

  &--ghost {
    color: $mauve;
    background: transparent;
    border-color: $indigo-velvet;

    &:hover:not(:disabled) {
      background: rgba($indigo-velvet, 0.4);
    }
  }

  &:disabled {
    cursor: not-allowed;
    opacity: 0.55;
  }

  &__spinner {
    width: 14px;
    height: 14px;
    border: 2px solid rgba(#fff, 0.4);
    border-top-color: #fff;
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
