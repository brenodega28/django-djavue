<template>
  <h1>{{name}}</h1>
</template>

<script>
import "imported"
import "nested/component-a"

export default {
    data: () => ({
        name: "$(name)"
    })
}
</script>

<style>
h1{
  color: 'red'
}
</style>