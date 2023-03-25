using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;


namespace Chess
{
    internal class Board
    {
        private Texture2D texture;
        private Vector2 loc;

        private List<Piece> white_pieces;
        private List<Piece> black_pieces;

        private BoardState boardState;

        private string first_move_square;
        private int square_index;

        public Board()
        {
            Globals.PieceTexture = Globals.Content.Load<Texture2D>("pieces");
            this.texture = Globals.Content.Load<Texture2D>("chessboard");
            this.loc = new Vector2(0, 0);

            this.NewGame(); // reset white and black pieces
            this.boardState = new BoardState(this.white_pieces, this.black_pieces);

            Debug.WriteLine(this.boardState.ToString());
        }

        public void NewGame()
        {
            this.white_pieces = new List<Piece>();
            this.black_pieces = new List<Piece>();

            this.square_index = 0;

            this.white_pieces.Add(new Piece(PieceType.White_Rook, "A1"));
            this.white_pieces.Add(new Piece(PieceType.White_Knight, "B1"));
            this.white_pieces.Add(new Piece(PieceType.White_Bishop, "C1"));
            this.white_pieces.Add(new Piece(PieceType.White_Queen, "D1"));
            this.white_pieces.Add(new Piece(PieceType.White_King, "E1"));
            this.white_pieces.Add(new Piece(PieceType.White_Bishop, "F1"));
            this.white_pieces.Add(new Piece(PieceType.White_Knight, "G1"));
            this.white_pieces.Add(new Piece(PieceType.White_Rook, "H1"));

            for (int i = 0; i < 8; i++)
            {
                this.white_pieces.Add(new Piece(PieceType.White_Pawn, ((char)('A' + i)).ToString() + '2'));
            }

            this.black_pieces.Add(new Piece(PieceType.Black_Rook, "A8"));
            this.black_pieces.Add(new Piece(PieceType.Black_Knight, "B8"));
            this.black_pieces.Add(new Piece(PieceType.Black_Bishop, "C8"));
            this.black_pieces.Add(new Piece(PieceType.Black_Queen, "D8"));
            this.black_pieces.Add(new Piece(PieceType.Black_King, "E8"));
            this.black_pieces.Add(new Piece(PieceType.Black_Bishop, "F8"));
            this.black_pieces.Add(new Piece(PieceType.Black_Knight, "G8"));
            this.black_pieces.Add(new Piece(PieceType.Black_Rook, "H8"));

            for (int i = 0; i < 8; i++)
            {
                this.black_pieces.Add(new Piece(PieceType.Black_Pawn, ((char)('A' + i)).ToString() + '7'));
            }
        }

        public void Move(string moveNotation)
        {
            this.boardState.Move(moveNotation);
        }

        public void Move(string square1, string square2)
        {
            this.boardState.Move(square1, square2);
        }

        public void LoadGame(List<string[]> moveSet)
        {
            this.NewGame();
            this.boardState = new BoardState(this.white_pieces, this.black_pieces);
        }

        private void MovePieces(string square1, string square2)
        {
            if(this.boardState.WhiteTurn)
            {
                for (int i = 0; i < this.white_pieces.Count; i++)
                {
                    if(this.white_pieces[i].GetSquare() == square1)
                    {

                    }
                }
            }
        }

        public void SelectSquare(string square)
        {
            if (this.square_index == 0)
            {
                this.first_move_square = square;
                this.square_index = 1;
            }
            else
            {
                this.boardState.Move(this.first_move_square, square);
                this.square_index = 0;
            }
        }

        public void Draw()
        {

            Globals.DrawBatch.Begin();
            Globals.DrawBatch.Draw(
                        this.texture,
                        this.loc,
                        new Rectangle(0, 0, 800, 800),
                        Color.White
                        );
            Globals.DrawBatch.End();
            
            this.boardState.DrawPieces();
        }

        public static string GetSquare(int row, int col)
        {
            return ((char)('A' + col)).ToString() + ((char)('8' - row)).ToString();
        }
    }
}
