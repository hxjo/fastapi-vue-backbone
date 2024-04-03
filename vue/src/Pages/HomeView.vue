<script setup lang="ts">
import TheWelcome from '../components/TheWelcome.vue'
import {Link} from "@inertiajs/vue3";

interface Props {
  message: string
}
const props = defineProps<Props>();
console.log(props.message)
</script>

<template>
  <main>
    <Link href="/about">About</Link>
    <TheWelcome />
  </main>
</template>
