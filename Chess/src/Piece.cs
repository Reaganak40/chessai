using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;

namespace Chess
{
    internal enum PieceType
    {
        None = 0,
        White_King,
        White_Queen,
        White_Rook,
        White_Bishop,
        White_Knight,
        White_Pawn,
        Black_King,
        Black_Queen,
        Black_Rook,
        Black_Bishop,
        Black_Knight,
        Black_Pawn,
    }
    internal class Piece
    {
        private PieceType type;
        private Texture2D texture;
        private int spriteSheetX;
        private int spriteSheetY;
        private string square;

        private int position;
        private Vector2 coords;


        public Piece(PieceType pieceType, string square)
        {
            this.square = square;
            this.type = pieceType;
            this.texture = Globals.Content.Load<Texture2D>("pieces");
            this.coords = new Vector2();

            this.Position = BoardState.GetIndexOfPositionArray(square);
            this.SetPiece(pieceType);
        }

        public int Position
        {
            get
            {
                return this.position;
            }

            set
            {
                if (this.position != value) 
                {
                    this.position = value;
                    this.coords.X = (position % 8) * 100;
                    this.coords.Y = (position / 8) * 100;
                }
            }
        }

        public void SetSquare(string square)
        {
            this.square = square;
        }

        public string GetSquare()
        {
            return this.square;
        }

        public void SetPiece(PieceType piece)
        {
            this.type = piece;

            switch (type)
            {
                case PieceType.White_King:
                    this.spriteSheetX = 0;
                    this.spriteSheetY = 0;
                    break;
                case PieceType.White_Queen:
                    this.spriteSheetX = 100;
                    this.spriteSheetY = 0;
                    break;
                case PieceType.White_Bishop:
                    this.spriteSheetX = 200;
                    this.spriteSheetY = 0;
                    break;
                case PieceType.White_Knight:
                    this.spriteSheetX = 300;
                    this.spriteSheetY = 0;
                    break;
                case PieceType.White_Rook:
                    this.spriteSheetX = 400;
                    this.spriteSheetY = 0;
                    break;
                case PieceType.White_Pawn:
                    this.spriteSheetX = 500;
                    this.spriteSheetY = 0;
                    break;
                case PieceType.Black_King:
                    this.spriteSheetX = 0;
                    this.spriteSheetY = 100;
                    break;
                case PieceType.Black_Queen:
                    this.spriteSheetX = 100;
                    this.spriteSheetY = 100;
                    break;
                case PieceType.Black_Bishop:
                    this.spriteSheetX = 200;
                    this.spriteSheetY = 100;
                    break;
                case PieceType.Black_Knight:
                    this.spriteSheetX = 300;
                    this.spriteSheetY = 100;
                    break;
                case PieceType.Black_Rook:
                    this.spriteSheetX = 400;
                    this.spriteSheetY = 100;
                    break;
                case PieceType.Black_Pawn:
                    this.spriteSheetX = 500;
                    this.spriteSheetY = 100;
                    break;
            }
        }

        public PieceType Type
        { 
            get
            {
                return this.type;
            }
        }

        

        public void Draw()
        {
            Globals.DrawBatch.Begin();
            Globals.DrawBatch.Draw(
                        this.texture,
                        this.coords,
                        new Rectangle(this.spriteSheetX, this.spriteSheetY, 100, 100),
                        Color.White
                        );
            Globals.DrawBatch.End();
        }
    }
}
