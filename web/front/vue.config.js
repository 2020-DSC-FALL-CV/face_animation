/*
:root {
    --main-primary: #0A4E9B;
    --main-secondary: #CADDDB;
    --main-black: #2B2926;
    --main-white: #fff;
    --main-lightGrey: #F2F2F2;
    --main-grey: #BDBDBD;
    --main-darkGrey: #828282;
    --main-green: #27AE60;
}
*/
module.exports = {
    css: {
        loaderOptions: {
            less: {
                lessOptions: {
                    modifyVars: {
                        'primary-color': '#0A4E9B',
                        'background-color-light': '#F2F2F2',
                        'menu-item-active-bg': '#CADDDB',
                        'menu-highlight-color': '#FFF',
                        'menu-color': "#BDBDBD",
                        'menu-item-color': "#BDBDBD",
                        "collapse-header-bg": "#F2F2F2",
                    },
                    javascriptEnabled: true,
                },
            },
        },
    },
};