<template>
  <div class="msg" :class="[`msg--${message.role}`, { 'msg--error': message.error }]">
    <div class="msg__bubble">
      {{ message.content }}
      <div v-if="message.sources?.length" class="msg__sources">
        Источники:
        <span v-for="s in message.sources" :key="s.article_id" class="msg__source">{{ s.title }}</span>
      </div>
    </div>
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
    color: $text;
    word-break: break-word;
    white-space: pre-wrap;
    border-radius: 14px;
  }

  &__sources {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    align-items: center;
    margin-top: 10px;
    font-size: 12px;
    color: $text-muted;
  }

  &__source {
    padding: 2px 8px;
    color: $green-700;
    background: $green-100;
    border-radius: 8px;
  }

  &--user &__bubble {
    background: $green-200;
    border: 1px solid $green-300;
    border-bottom-right-radius: 4px;
  }

  &--assistant &__bubble {
    background: $surface;
    border: 1px solid $border;
    border-bottom-left-radius: 4px;
    box-shadow: 0 1px 4px rgba($green-700, 0.06);
  }

  &--error &__bubble {
    color: $error-text;
    background: $error-bg;
    border-color: $error-border;
  }
}
</style>
