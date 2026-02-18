return {
  {
    "sainnhe/everforest",
    priority = 1000,
    init = function()
      vim.o.background = "light"
    end,
  },
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "everforest",
    },
  },
}
