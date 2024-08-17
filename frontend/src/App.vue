<template>
  <div id="app">
    <router-view></router-view> <!-- 라우터에서 설정한 컴포넌트를 여기에 표시 -->
  </div>
</template>

<script>
export default {
  setup() {
    // 별도의 로직 필요 없음
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
}
</style>
