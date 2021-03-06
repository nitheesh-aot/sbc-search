// import "vuetify/dist/vuetify.min.css";
import "material-design-icons-iconfont/dist/material-design-icons.css";
import Vue from "vue";
import Vuetify from "vuetify/lib";

Vue.use(Vuetify);

export default new Vuetify({
  icons: {
    iconfont: "md"
  },
  theme: {
    options: {
      customProperties: true
    },
    themes: {
      light: {
        primary: "#2076d2",
        secondary: "#424242",
        accent: "#09A4DC",
        error: "#FF5252",
        info: "#2196F3",
        success: "#4CAF50",
        warning: "#fb8c00"
      }
    }
  }
});
