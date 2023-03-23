using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using System.Diagnostics;

namespace Chess
{
    public class Chess : Game
    {
        private GraphicsDeviceManager _graphics;
        private SpriteBatch _spriteBatch;
        private Controller controller;

        public Chess()
        {
            _graphics = new GraphicsDeviceManager(this);
            Content.RootDirectory = "Content";
            
            IsMouseVisible = true;
            this._graphics.IsFullScreen = false;
            this._graphics.PreferredBackBufferWidth = 800;
            this._graphics.PreferredBackBufferHeight = 800;
            Globals.WindowWidth = this._graphics.PreferredBackBufferWidth;
            Globals.WindowHeight = this._graphics.PreferredBackBufferHeight;
            
        }

        protected override void Initialize()
        {
            // TODO: Add your initialization logic here
            Globals.Content = this.Content;

            this.controller = new Controller();

            base.Initialize();
        }

        protected override void LoadContent()
        {
            this._spriteBatch = new SpriteBatch(GraphicsDevice);
            Globals.DrawBatch = _spriteBatch;


            // TODO: use this.Content to load your game content here
        }

        protected override void Update(GameTime gameTime)
        {
            if (GamePad.GetState(PlayerIndex.One).Buttons.Back == ButtonState.Pressed || Keyboard.GetState().IsKeyDown(Keys.Escape))
                Exit();

            // TODO: Add your update logic here

            if (this.IsActive)
            {
                this.controller.Update();
            }

            base.Update(gameTime);
        }

        protected override void Draw(GameTime gameTime)
        {
            GraphicsDevice.Clear(Color.CornflowerBlue);

            // TODO: Add your drawing code here
            this.controller.Draw();

            base.Draw(gameTime);
        }
    }
}