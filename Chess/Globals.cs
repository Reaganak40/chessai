using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Content;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;

namespace Chess
{
    internal static class Globals
    {
        public static SpriteBatch DrawBatch { get; set; }

        /// <summary>
        /// Gets or sets the location and manager of sprite assets.
        /// </summary>
        public static ContentManager Content { get; set; }

        /// <summary>
        /// Gets or sets the Window Width of the game screen.
        /// </summary>
        public static int WindowWidth { get; set; }

        /// <summary>
        /// Gets or sets Window Width of the game screen.
        /// </summary>
        public static int WindowHeight { get; set; }

        public static Texture2D PieceTexture { get; set; }

        public static GameWindow Window { get; set; }

        public static void SetTitle(string title)
        {
            Globals.Window.Title = title;
        }

    }
}
