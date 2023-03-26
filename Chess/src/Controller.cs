using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;

using System.IO;
namespace Chess
{
    internal class Controller
    {
        private Board chessboard;
        private MouseState lastMouseState;
        private MouseState currentMouseState;
        
        private KeyboardState currentKeyState;
        private KeyboardState oldKeyState;

        private string pathToPGN;

        private List<string[]> moves;
        private int move_index;
        private int turn;

        public Controller(string pathToPGN=null)
        {
            chessboard = new Board();
            this.currentMouseState = Mouse.GetState();

            this.currentKeyState = Keyboard.GetState();
            this.oldKeyState = this.currentKeyState;


            if (pathToPGN != null ) 
            {
                this.pathToPGN = Directory.GetParent(Environment.CurrentDirectory).Parent.Parent.FullName + "/" + pathToPGN;
                this.pathToPGN = this.pathToPGN.Replace("\\", "/");
                Debug.WriteLine(this.pathToPGN);
            }
            else
            {
                this.pathToPGN = pathToPGN;
            }
            this.move_index = 0;
            this.turn = 0;
        }

        public void Load()
        {
            if (this.pathToPGN != null)
            {
                if (File.Exists(this.pathToPGN))
                {
                    string gameName = Path.GetFileName(this.pathToPGN).Split(".")[0];
                    Globals.SetTitle("Game Replay - " + gameName);
                    this.moves = PGNReader.ReadPGN(this.pathToPGN);
                    this.chessboard.LoadGame(this.moves);
                }
                else
                {
                    Globals.SetTitle("Game Replay - File Not Found");
                }
            }
        }

        public void Update()
        {
            this.lastMouseState = this.currentMouseState;
            this.currentMouseState = Mouse.GetState();


            var mousePosition = new Point(currentMouseState.X, currentMouseState.Y);

            
            // handle the input
            this.currentKeyState = Keyboard.GetState();
            if (oldKeyState.IsKeyUp(Keys.Right) && currentKeyState.IsKeyDown(Keys.Right))
            {
                if (!this.moves[this.move_index][this.turn].Equals("*"))
                {
                    this.chessboard.Move(this.moves[this.move_index][this.turn]);
                    if (this.turn == 1)
                    {
                        move_index += 1;
                        this.turn = 0;
                    }
                    else
                    {
                        this.turn = 1;
                    }
                }
            }
            else if (oldKeyState.IsKeyUp(Keys.Left) && currentKeyState.IsKeyDown(Keys.Left))
            {
                move_index -= 1;
            }
            this.oldKeyState = this.currentKeyState;


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
