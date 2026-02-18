return {
  {
    "sainnhe/everforest",
    priority = 1000,
    config = function()
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
