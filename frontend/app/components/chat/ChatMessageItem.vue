<template>
  <div class="msg" :class="[`msg--${message.role}`, { 'msg--error': message.error }]">
    <div class="msg__bubble">{{ message.content }}</div>
  </div>
</template>

<script setup lang="ts">
import type { ChatMessage } from '~/types'

defineProps<{
  message: ChatMessage
}>()
</script>

<style lang="scss" scoped>
.msg {
  display: flex;

  &--user {
    justify-content: flex-end;
  }

  &--assistant {
    justify-content: flex-start;
  }

  &__bubble {
    max-width: min(720px, 85%);
    padding: 12px 16px;
    line-height: 1.5;
    color: #fff;
    word-break: break-word;
    white-space: pre-wrap;
    border-radius: 14px;
  }

  &--user &__bubble {
    background: $royal-violet;
    border-bottom-right-radius: 4px;
  }

  &--assistant &__bubble {
    background: rgba($indigo-ink, 0.6);
    border: 1px solid $indigo-velvet;
    border-bottom-left-radius: 4px;
  }

  &--error &__bubble {
    color: #ffb4c0;
    background: rgba(#ff4d6d, 0.15);
    border-color: rgba(#ff4d6d, 0.4);
  }
}
</style>
