<template>
  <v-text-field
    background-color="#e5e8ec"
    class="search-input search-input-corporation"
    label="Search Term"
    :height="height"
    v-model="searchQuery"
    placeholder="Corporation Name or Number"
    filled
  />
</template>

<script>
export default {
  props: {
    height: {
      default: 40.8,
      type: Number
    },
    props: {
      query: {
        default: null,
        type: String
      }
    }
  },
  data() {
    return {
      searchQuery: this.query
    };
  },
  mounted() {
    this.$root.$on("setCorpSearchInput", r => (this.searchQuery = r));
  },
  methods: {
    clear() {
      this.searchQuery = "";
    }
  },
  watch: {
    searchQuery(nq) {
      this.$emit("update:query", nq);
    }
  }
};
</script>
<style lang="scss">
.search-input-corporation {
  width: 250px;
}
@media (max-width: 959px) {
  .search-input {
    width: 100% !important;
  }
}
</style>
