
<script setup lang="ts">
import {Link} from "@inertiajs/vue3";

interface Props {
  message: string
}
const props = defineProps<Props>();
console.log(props.message)
</script>

<template>
  <div class="about">
    <Link href="/">Home</Link>
    <h1>This is an about page</h1>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>