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
    color: #fff;
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
    color: rgba(#fff, 0.6);
  }

  &__source {
    padding: 2px 8px;
    background: rgba($indigo-velvet, 0.5);
    border-radius: 8px;
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
