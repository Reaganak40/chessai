using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Chess
{
    internal class Controller
    {
        private Board chessboard;
        private MouseState lastMouseState;
        private MouseState currentMouseState;



        public Controller()
        {

            chessboard = new Board();
            this.currentMouseState = Mouse.GetState();

        }

        public void Load()
        {
            
        }

        public void Update()
        {
            this.lastMouseState = this.currentMouseState;
            this.currentMouseState = Mouse.GetState();

            var mousePosition = new Point(currentMouseState.X, currentMouseState.Y);


            if (currentMouseState.LeftButton == ButtonState.Released)
            {
                if (lastMouseState.LeftButton == ButtonState.Pressed)
                {
                    int end_x = mousePosition.X / 100;
                    int end_y = mousePosition.Y / 100;

                    /*if (!(end_x < 0 || end_x > 8) || (end_y < 0 || end_y > 8))
                    {
                        this.chessboard.SelectSquare(Piece.GetSquare(end_y, end_x));
                    }*/

                }    

            }
        }

        public void Draw()
        {
            this.chessboard.Draw();
        }
    }
}
