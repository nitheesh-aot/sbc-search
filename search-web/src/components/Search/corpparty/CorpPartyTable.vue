<template>
  <div>
    <v-data-table
      v-if="qs"
      mobile-breakpoint="960"
      class="elevation-1 corp-party-table"
      :headers="headers"
      :items="results"
      :fixed-header="true"
      :options.sync="options"
      :server-items-length="totalItems"
      :loading="loading"
      :disable-sort="disableSorting"
      @update:sort-by="updateSort"
      @update:sort-desc="updateSort"
      :sort-by="sortBy"
      :sort-desc="sortDesc"
      :footer-props="{
        'items-per-page-options': [50]
      }"
    >
      <template v-slot:top="{}">
        <div>
          <div
            v-if="items.length === 0"
            class="v-data-footer v-data-custom-header"
          >
            <div class="v-data-footer__pagination">&ndash;</div>
          </div>
          <div v-else class="v-data-footer v-data-custom-header">
            <div class="v-data-footer__pagination">
              <div
                class="w-100 custom-footer d-flex justify-end align-center caption"
              >
                <div class="letter-spacing-none">
                  Showing {{ showingMin }}-{{ showingMax }} of
                  {{ totalItems }} results
                </div>
                <div class="d-flex ml-5 align-center">
                  <v-btn
                    v-if="page > '1' && !loading"
                    icon
                    @click="pagePrev"
                    small
                  >
                    <v-icon>arrow_back</v-icon>
                  </v-btn>
                  <v-btn v-else disabled icon small>
                    <v-icon>arrow_back</v-icon>
                  </v-btn>
                  <div class="d-inline-block mr-3 ml-3 letter-spacing-none">
                    Page {{ page }}
                  </div>
                  <v-btn
                    icon
                    v-if="showingMax < totalItems && !loading"
                    @click="pageNext"
                    small
                  >
                    <v-icon>arrow_forward</v-icon>
                  </v-btn>
                  <v-btn icon v-else disabled small>
                    <v-icon>arrow_forward</v-icon>
                  </v-btn>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
      <template v-slot:item="{ item, index, headers }">
        <!-- Mobile View Begin -->
        <tr
          class="cursor-pointer d-table-row d-md-none mobile-tr-row"
          v-for="(value, i) in Object.values(orderItems(item))"
          :key="`row${index}${value}${i}`"
        >
          <td
            v-if="headers[i] && headers[i].value === 'corpNum'"
            class="d-table-cell"
            @click.prevent.stop="handleCorpClick(item['corpNum'], $event)"
          >
            <div class="d-flex w-100 justify-space-between">
              <div class="color-black">
                {{ headers[i] ? headers[i].text : "" }}
              </div>
              <div class="text-right anchor-text cursor-pointer">
                {{ value }}
              </div>
            </div>
          </td>
          <td
            v-else
            class="d-table-cell"
            @click="handleCellClick(item['corpPartyId'], $event)"
          >
            <div class="d-flex w-100 justify-space-between">
              <div class="color-black">
                {{ headers[i] ? headers[i].text : "" }}
              </div>
              <div class="text-right">{{ value }}</div>
            </div>
          </td>
        </tr>
        <v-divider class="d-md-none" />
        <!-- Mobile View End -->

        <tr
          class="cursor-pointer d-none d-md-table-row desktop-tr-row"
          @click="handleCellClick(item['corpPartyId'], $event)"
        >
          <td>{{ item["lastNme"] }}</td>
          <td>{{ item["firstNme"] }}</td>
          <td>{{ item["middleNme"] }}</td>
          <td v-if="type === 'addr'">{{ item["addr"] }}</td>
          <td v-if="type === 'addr'">{{ item["postalCd"] }}</td>
          <td>{{ item["partyTypCd"] }}</td>
          <td>{{ item["appointmentDt"] }}</td>
          <td>{{ item["cessationDt"] }}</td>
          <td v-if="type === 'active'">{{ item["stateTypCd"] }}</td>
          <td>{{ item["corpNme"] }}</td>
          <td @click.prevent.stop="handleCorpClick(item['corpNum'], $event)">
            <span class="anchor-text cursor-pointer">{{
              item["corpNum"]
            }}</span>
          </td>
        </tr>
      </template>
      <template v-slot:footer>
        <v-progress-linear
          :active="loading"
          :indeterminatev-data-table__wrapp="true"
          color="primary"
          height="2"
        ></v-progress-linear>
      </template>
      <template v-slot:footer.page-text="{}">
        <div class="custom-footer d-flex align-center">
          <div>
            Showing {{ showingMin }}-{{ showingMax }} of
            {{ totalItems }} results
          </div>
          <div class="d-flex ml-5 align-center">
            <v-btn v-if="page > '1' && !loading" icon @click="pagePrev" small>
              <v-icon>arrow_back</v-icon>
            </v-btn>
            <v-btn v-else disabled icon small>
              <v-icon>arrow_back</v-icon>
            </v-btn>
            <div class="d-inline-block mr-3 ml-3">Page {{ page }}</div>
            <v-btn
              icon
              v-if="showingMax < totalItems && !loading"
              @click="pageNext"
              small
            >
              <v-icon>arrow_forward</v-icon>
            </v-btn>
            <v-btn icon v-else disabled small>
              <v-icon>arrow_forward</v-icon>
            </v-btn>
          </div>
        </div>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import { CORPPARTY_HEADERS } from "@/config/index.ts";
import axios from "axios";
import { corpPartySearch } from "@/api/SearchApi.js";
import dayjs from "dayjs";
import { mapGetters } from "vuex";
import { buildQueryString } from "@/util/index.ts";
import isEmpty from "lodash-es/isEmpty";
import pick from "lodash-es/pick";
const qsl = require("qs");
export default {
  props: {
    qs: {
      default: null,
      type: String
    },
    type: {
      default: "none",
      type: String
    },
    page: {
      default: "1",
      type: String
    }
  },
  computed: {
    headers() {
      return this.filterHeaders(CORPPARTY_HEADERS, this.type);
    },
    showingMin() {
      if (this.page == 1) {
        return 1;
      }
      let min = 0;
      for (let i = 0; i < this.page - 1; i++) {
        min += this.items_per_page;
      }
      return min;
    },
    showingMax() {
      if (this.items.length < this.items_per_page && this.page == 1) {
        return this.items.length;
      }
      if (this.items.length < this.items_per_page && this.page != 1) {
        return this.showingMin + this.items.length;
      }
      return this.page * this.items_per_page;
    },
    results() {
      return this.items.map(r => {
        if (r["appointmentDt"]) {
          r["appointmentDt"] = dayjs(r["appointmentDt"]).format("YYYY-MM-DD");
        } else {
          r["appointmentDt"] = "-";
        }

        if (r["cessationDt"]) {
          r["cessationDt"] = dayjs(r["cessationDt"]).format("YYYY-MM-DD");
        } else {
          r["cessationDt"] = "-";
        }

        return r;
      });
    },
    ...mapGetters({
      filters: "corpParty/filters/getFilters",
      numFilters: "corpParty/filters/getNumFilters"
    })
  },
  data() {
    return {
      items: [],
      options: {},
      loading: true,
      totalItems: 0,
      disableSorting: false,
      sortBy: [],
      sortDesc: [],
      items_per_page: 50,
      source: null
    };
  },
  methods: {
    orderItems(items) {
      return pick(items, [
        "lastNme",
        "firstNme",
        "middleNme",
        "addr",
        "postalCd",
        "partyTypCd",
        "appointmentDt",
        "cessationDt",
        "stateTypCd",
        "corpNme",
        "corpNum"
      ]);
    },
    pageNext() {
      this.$emit("pageUpdate", (parseInt(this.page) + 1).toString());
    },
    pagePrev() {
      if (this.page > "1") {
        this.$emit("pageUpdate", (parseInt(this.page) - 1).toString());
      }
    },
    updateSort() {
      this.$emit("sortUpdate", {
        sortBy: this.options.sortBy,
        sortDesc: this.options.sortDesc
      });
    },
    handleCorpClick(id, e) {
      e.target.closest("tr").classList.add("row-clicked");
      if (window.getSelection().toString()) {
        return;
      }
      this.$router.push("/corporation/" + id);
      return;
    },
    handleCellClick(id, e) {
      e.target.closest("tr").classList.add("row-clicked");
      if (window.getSelection().toString()) {
        return;
      }
      this.$router.push("/corpparty/" + id);
      return;
    },
    filterHeaders(headers, type) {
      if (type === "none") {
        return headers.filter(h => {
          const val = h.value;
          if (
            val === "lastNme" ||
            val === "middleNme" ||
            val === "firstNme" ||
            val === "partyTypCd" ||
            val === "appointmentDt" ||
            val === "cessationDt" ||
            val === "corpNme" ||
            val === "corpNum"
          ) {
            return true;
          }
          return false;
        });
      } else if (type === "addr") {
        return headers.filter(h => {
          const val = h.value;
          if (
            val === "lastNme" ||
            val === "middleNme" ||
            val === "firstNme" ||
            val === "partyTypCd" ||
            val === "appointmentDt" ||
            val === "cessationDt" ||
            val === "corpNum" ||
            val === "corpNme" ||
            val === "addr" ||
            val === "postalCd"
          ) {
            return true;
          }
          return false;
        });
      } else if (type === "active") {
        return headers.filter(h => {
          const val = h.value;
          if (
            val === "lastNme" ||
            val === "middleNme" ||
            val === "firstNme" ||
            val === "partyTypCd" ||
            val === "appointmentDt" ||
            val === "cessationDt" ||
            val === "corpNum" ||
            val === "corpNme" ||
            val === "stateTypCd"
          ) {
            return true;
          }
          return false;
        });
      }
    },
    cancelRequest() {
      this.source && this.source.cancel("Request aborted by user");
    },
    fetchData() {
      if (!this.qs) {
        return;
      }

      this.loading = true;
      this.disableSorting = true;

      let queryString = this.qs;
      const { sort_type, sort_value } = qsl.parse(queryString);
      if (sort_type && sort_value) {
        this.sortBy = [sort_value];
        if (sort_type === "asc") {
          this.sortDesc = [false];
        } else if (sort_type === "dsc") {
          this.sortDesc = [true];
        }
      }

      const CancelToken = axios.CancelToken;
      this.source = CancelToken.source();

      corpPartySearch(queryString, {
        cancelToken: this.source.token
      })
        .then(result => {
          this.items = result.data.results;
          this.totalItems = result.data.numResults;
          this.$emit("success", result);
          this.totalItems >= 165 ? this.$emit("overload") : "";
        })
        .catch(e => {
          this.items = [];
          this.totalItems = 0;
          this.$emit("error", e);
        })
        .finally(() => {
          this.loading = false;
          this.disableSorting = false;
        });
    }
  },
  watch: {
    qs(nq) {
      this.fetchData();
    }
  }
};
</script>

<style lang="scss">
.corp-party-table th:first-of-type,
.corp-party-table td:first-of-type {
  color: rgba(0, 0, 0, 0.6) !important;
}

.corp-party-table .custom-footer {
  padding: 1em 0;
  letter-spacing: 0 !important;
}

.corp-party-table .v-data-footer__icons-after,
.corp-party-table .v-data-footer__icons-before {
  display: none;
}

.mobile-tr-row,
.mobile-tr-row td {
  border-bottom: 0 !important;
}

.row-clicked {
  background-color: $COLOR_LAVENDER !important;
}

.corp-party-table {
  box-shadow: inset -5px 0px 5px 0px rgba(0, 0, 0, 0.75) !important;
}

.v-application--is-ltr .v-data-table--fixed-header .v-data-footer {
  margin-right: 0px !important;
}

.v-data-custom-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

.corp-party-table .v-data-table__wrapper {
  overflow-x: auto;
  background-image: linear-gradient(to right, #ffffff, rgba(255, 255, 255, 0)),
    linear-gradient(to left, #ffffff, rgba(255, 255, 255, 0)),
    linear-gradient(to right, #e0e0e0, rgba(0, 0, 0, 0)),
    linear-gradient(to left, #e0e0e0, rgba(0, 0, 0, 0));
  background-position: 0 0, 100% 0, 0 0, 100% 0;
  background-repeat: no-repeat;
  background-color: white;
  background-size: 4em 100%, 4em 100%, 2em 100%, 2em 100%;
  background-attachment: local, local, scroll, scroll;
}
</style>
